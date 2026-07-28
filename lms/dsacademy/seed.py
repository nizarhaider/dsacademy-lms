"""Idempotently configure a Frappe site as DS Academy."""

import json
from pathlib import Path

import frappe
from frappe.utils import nowdate
from frappe.utils.file_manager import save_file

from lms.dsacademy.curriculum import COURSE, WEEKS
from lms.lms.doctype.lms_course.lms_course import update_course_statistics

ASSET_URL = "/assets/lms"
MEDIA_ROOT = Path(frappe.get_app_path("lms", "public", "course-media"))
MEDIA_VERSION = "20260728-beginner-ai-18-week-v1"
LEGACY_COURSE_TITLES = (
	"End-to-End Data Science & AI",
	"Production AI Engineering Bootcamp",
)


def seed_all():
	"""Create or update branding, settings, instructor, and flagship course."""
	frappe.set_user("Administrator")
	configure_system()
	configure_branding()
	configure_lms()
	instructor = upsert_instructor()
	course = upsert_course(instructor)

	chapter_names = []
	for week_number, week_data in enumerate(WEEKS, start=1):
		chapter = upsert_chapter(course, week_number, week_data)
		chapter_names.append(chapter.name)
		lesson_names = []
		for session_number, session_data in enumerate(week_data["sessions"], start=1):
			lesson = upsert_session_lesson(
				course,
				chapter,
				week_number,
				session_number,
				session_data,
			)
			lesson_names.append(lesson.name)
		assessment = upsert_assessment_lesson(
			course, chapter, week_number, week_data
		)
		lesson_names.append(assessment.name)
		chapter.set("lessons", [{"lesson": name} for name in lesson_names])
		chapter.save(ignore_permissions=True)

	course.set("chapters", [{"chapter": name} for name in chapter_names])
	course.save(ignore_permissions=True)

	update_course_statistics()
	frappe.db.commit()
	return {
		"course": course.name,
		"chapters": len(WEEKS),
		"lessons": sum(len(item["sessions"]) + 1 for item in WEEKS),
		"quizzes": len(WEEKS),
		"assignments": len(WEEKS),
	}


def configure_system():
	system_settings = frappe.get_single("System Settings")
	system_settings.update(
		{
			"country": "Sri Lanka",
			"language": "en",
			"time_zone": "Asia/Colombo",
			"setup_complete": 1,
		}
	)
	system_settings.save(ignore_permissions=True)
	frappe.db.set_value(
		"Installed Application",
		{"app_name": "frappe"},
		"is_setup_complete",
		1,
	)


def get_seed_counts():
	"""Return database counts for the owned curriculum records."""
	course = frappe.db.get_value("LMS Course", {"title": COURSE["title"]}, "name")
	quiz_names = frappe.get_all(
		"LMS Quiz",
		{"course": course},
		pluck="name",
	)
	return {
		"courses": frappe.db.count("LMS Course", {"name": course}),
		"chapters": frappe.db.count("Course Chapter", {"course": course}),
		"lessons": frappe.db.count("Course Lesson", {"course": course}),
		"quizzes": len(quiz_names),
		"quiz_rows": frappe.db.count("LMS Quiz Question", {"parent": ["in", quiz_names]}),
		"questions": frappe.db.count("LMS Question", {"question": ["like", "W%Q%:%"]}),
		"assignments": frappe.db.count("LMS Assignment", {"course": course}),
	}


def configure_branding():
	settings = frappe.get_single("Website Settings")
	settings.app_name = "DS Academy"
	settings.home_page = "lms"
	settings.banner_image = ensure_file(
		"dsacademy-logo-light.png", "images/dsacademy/logo-light.png"
	)
	settings.footer_logo = ensure_file(
		"dsacademy-logo-dark.png", "images/dsacademy/logo-dark.png"
	)
	settings.app_logo = settings.banner_image
	settings.favicon = ensure_file("dsacademy-mark.png", "images/dsacademy/mark.png")
	settings.save(ignore_permissions=True)
	# The LMS home is a client-side route, so Website Settings validation cannot resolve it.
	frappe.db.set_single_value("Website Settings", "home_page", "lms")


def ensure_file(file_name, relative_path):
	existing = frappe.db.get_value(
		"File",
		{
			"file_name": file_name,
			"attached_to_doctype": "Website Settings",
			"attached_to_name": "Website Settings",
		},
		"file_url",
	)
	if existing:
		return existing

	content = Path(frappe.get_app_path("lms", "public", relative_path)).read_bytes()
	file_doc = save_file(
		file_name,
		content,
		"Website Settings",
		"Website Settings",
		is_private=0,
	)
	return file_doc.file_url


def configure_lms():
	settings = frappe.get_single("LMS Settings")
	settings.update(
		{
			"allow_guest_access": 1,
			"default_home": 1,
			"disable_signup": 0,
			"show_dashboard": 1,
			"show_courses": 1,
			"show_students": 1,
			"show_assessments": 1,
			"show_live_class": 1,
			"show_discussions": 1,
			"show_emails": 1,
			"courses": 1,
			"batches": 1,
			"certifications": 1,
			"programming_exercises": 1,
			"jobs": 0,
			"statistics": 1,
			"notifications": 1,
			"enforce_video_completion": 0,
			"enforce_quiz_completion": 1,
			"enforce_assignment_completion": 1,
			"lesson_dwell_time": 30,
			"meta_description": (
				"Practical English AI engineering training in local models, "
				"RAG, agents, evaluation, MLOps, and production deployment."
			),
			"meta_keywords": (
				"AI engineering Sri Lanka, LLM course, RAG course, AI agents, "
				"LangGraph, MCP, MLOps, Python"
			),
			"meta_image": f"{ASSET_URL}/images/dsacademy/course-cover.png",
			"contact_us_email": "nizarhaider@gmail.com",
			"contact_us_url": "https://dsacademy.lk",
		}
	)
	settings.save(ignore_permissions=True)


def upsert_instructor():
	email = "instructor@dsacademy.lk"
	if frappe.db.exists("User", email):
		instructor = frappe.get_doc("User", email)
	else:
		instructor = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": "DS Academy",
				"last_name": "Faculty",
				"enabled": 1,
				"user_type": "System User",
				"send_welcome_email": 0,
			}
		).insert(ignore_permissions=True)

	for role in ("Moderator", "Course Creator"):
		if role not in frappe.get_roles(instructor.name):
			instructor.add_roles(role)
	return instructor


def upsert_course(instructor):
	name = frappe.db.exists("LMS Course", {"title": COURSE["title"]})
	if not name:
		for legacy_title in LEGACY_COURSE_TITLES:
			name = frappe.db.exists("LMS Course", {"title": legacy_title})
			if name:
				break
	course = frappe.get_doc("LMS Course", name) if name else frappe.new_doc("LMS Course")
	course.update(
		{
			**COURSE,
			"category": ensure_category(),
			"published": 1,
			"published_on": nowdate(),
			"status": "Approved",
			"featured": 1,
			"disable_self_learning": 0,
			"upcoming": 0,
			"enable_certification": 1,
			"paid_course": 0,
			"paid_certificate": 0,
			"image": f"{ASSET_URL}/images/dsacademy/course-cover.png",
			"card_gradient": "Cyan",
			"instructors": [{"instructor": instructor.name}],
		}
	)
	course.save(ignore_permissions=True)
	return course


def ensure_category():
	category = "AI Engineering"
	if not frappe.db.exists("LMS Category", category):
		frappe.get_doc({"doctype": "LMS Category", "category": category}).insert(
			ignore_permissions=True
		)
	return category


def upsert_chapter(course, week_number, week_data):
	title = f"Module {week_number:02d} · {week_data['title']}"
	name = frappe.db.exists("Course Chapter", {"course": course.name, "title": title})
	chapter = (
		frappe.get_doc("Course Chapter", name)
		if name
		else frappe.new_doc("Course Chapter")
	)
	chapter.update({"course": course.name, "title": title})
	chapter.save(ignore_permissions=True)
	append_once(course, "chapters", "chapter", chapter.name)
	return chapter


def upsert_session_lesson(
	course,
	chapter,
	week_number,
	session_number,
	session_data,
):
	title = f"{session_number}. {session_data['title']}"
	name = frappe.db.exists(
		"Course Lesson",
		{"course": course.name, "chapter": chapter.name, "title": title},
	)
	lesson = (
		frappe.get_doc("Course Lesson", name)
		if name
		else frappe.new_doc("Course Lesson")
	)
	lesson.update(
		{
			"course": course.name,
			"chapter": chapter.name,
			"title": title,
			"include_in_preview": week_number == 1 and session_number == 1,
			"body": render_lesson_body(
				week_number,
				session_number,
				session_data,
			),
			"content": None,
		}
	)
	lesson.save(ignore_permissions=True)
	append_once(chapter, "lessons", "lesson", lesson.name)
	return lesson


def upsert_assessment_lesson(course, chapter, week_number, week_data):
	quiz = upsert_quiz(course, week_number, week_data)
	assignment = upsert_assignment(course, week_number, week_data)
	title = f"{len(week_data['sessions']) + 1}. Module Assessment & Portfolio Project"
	content = {
		"time": 0,
		"blocks": [
			{
				"id": f"module-{week_number:02d}-quiz",
				"type": "quiz",
				"data": {"quiz": quiz.name},
			},
			{
				"id": f"module-{week_number:02d}-assignment",
				"type": "assignment",
				"data": {"assignment": assignment.name},
			},
		],
		"version": "2.29.0",
	}
	name = frappe.db.exists(
		"Course Lesson",
		{"course": course.name, "chapter": chapter.name, "title": title},
	)
	lesson = (
		frappe.get_doc("Course Lesson", name)
		if name
		else frappe.new_doc("Course Lesson")
	)
	lesson.update(
		{
			"course": course.name,
			"chapter": chapter.name,
			"title": title,
			"body": None,
			"content": json.dumps(content),
		}
	)
	lesson.save(ignore_permissions=True)
	append_once(chapter, "lessons", "lesson", lesson.name)
	return lesson


def upsert_quiz(course, week_number, week_data):
	title = f"Module {week_number:02d} Knowledge Check"
	name = frappe.db.exists("LMS Quiz", {"title": title})
	quiz = frappe.get_doc("LMS Quiz", name) if name else frappe.new_doc("LMS Quiz")
	question_rows = []

	for index, (prompt, options, correct_index) in enumerate(
		week_data["quiz"],
		start=1,
	):
		question_title = f"W{week_number:02d}Q{index}: {prompt}"
		question_name = frappe.db.exists(
			"LMS Question",
			{"question": question_title},
		)
		question = (
			frappe.get_doc("LMS Question", question_name)
			if question_name
			else frappe.new_doc("LMS Question")
		)
		values = {"question": question_title, "type": "Choices"}
		for option_index, option in enumerate(options, start=1):
			values[f"option_{option_index}"] = option
			values[f"is_correct_{option_index}"] = option_index - 1 == correct_index
		question.update(values)
		question.save(ignore_permissions=True)
		question_rows.append({"question": question.name, "marks": 5})

	quiz.update(
		{
			"title": title,
			"passing_percentage": 70,
			"max_attempts": 3,
			"show_answers": 1,
			"show_submission_history": 1,
			"shuffle_questions": 1,
			"course": course.name,
			"questions": question_rows,
		}
	)
	quiz.save(ignore_permissions=True)
	return quiz


def upsert_assignment(course, week_number, week_data):
	assignment_title, question, rubric = week_data["assignment"]
	title = f"Module {week_number:02d}: {assignment_title}"
	name = frappe.db.exists("LMS Assignment", {"title": title})
	assignment = (
		frappe.get_doc("LMS Assignment", name)
		if name
		else frappe.new_doc("LMS Assignment")
	)
	assignment.update(
		{
			"title": title,
			"type": "Document",
			"course": course.name,
			"question": (
				f"<p>{question}</p><p><strong>Assessment rubric:</strong> "
				f"{rubric}</p>"
			),
		}
	)
	assignment.save(ignore_permissions=True)
	return assignment


def render_lesson_body(week_number, session_number, session_data):
	slug = f"module-{week_number:02d}/lesson-{session_number:02d}"
	lines = [
		f"# {session_data['title']}",
		"",
		"## Learning outcomes",
		"",
		*[f"- {item}" for item in session_data["outcomes"]],
		"",
		"## Core concepts",
		"",
		", ".join(session_data["concepts"]).capitalize() + ".",
		"",
		"## Guided lab",
		"",
		session_data["lab"],
		"",
		"## Portfolio deliverable",
		"",
		session_data["deliverable"],
		"",
		"## Narrated explanation",
		"",
		session_data["narration_en"],
	]

	for label, relative_path, macro in [
		("Lesson audio", f"{slug}/narration-en.mp3", "Audio"),
		("Lesson slides", f"{slug}/slides.pdf", "PDF"),
		("Lesson video", f"{slug}/lesson-en.mp4", "Video"),
	]:
		if (MEDIA_ROOT / relative_path).exists():
			lines.extend(
				[
					"",
					f"### {label}",
					"",
					f'{{{{ {macro}("{ASSET_URL}/course-media/{relative_path}?v={MEDIA_VERSION}") }}}}',
				]
			)
	powerpoint_path = f"{slug}/slides.pptx"
	if (MEDIA_ROOT / powerpoint_path).exists():
		lines.extend(
			[
				"",
				f"[Download the editable PowerPoint deck]({ASSET_URL}/course-media/{powerpoint_path}?v={MEDIA_VERSION})",
			]
		)
	guided_notebook_path = f"{slug}/guided-lab.ipynb"
	if (MEDIA_ROOT / guided_notebook_path).exists():
		lines.extend(
			[
				"",
				f"[Download the guided notebook]({ASSET_URL}/course-media/{guided_notebook_path}?v={MEDIA_VERSION})",
			]
		)
	return "\n".join(lines)


def append_once(parent, table_field, link_field, value):
	parent.reload()
	if not any(row.get(link_field) == value for row in parent.get(table_field)):
		parent.append(table_field, {link_field: value})
		parent.save(ignore_permissions=True)
