"""Contract tests for the versioned DS Academy curriculum."""

import unittest

from lms.dsacademy.curriculum import COURSE, WEEKS
from lms.dsacademy.deck_content import build_slide_outline


class CurriculumContractTest(unittest.TestCase):
	def test_program_shape(self):
		self.assertEqual(len(WEEKS), 18)
		self.assertEqual(
			[len(week["sessions"]) for week in WEEKS],
			[1] * 18,
		)
		self.assertEqual(sum(len(week["sessions"]) for week in WEEKS), 18)
		self.assertEqual(sum(len(week["quiz"]) for week in WEEKS), 54)
		self.assertEqual(COURSE["title"], "AI Engineering Bootcamp")
		self.assertIn("English", COURSE["description"])
		self.assertEqual(COURSE["source_license"], "MIT")
		self.assertEqual(COURSE["duration_weeks"], 18)
		self.assertEqual(COURSE["weekly_minutes"], 180)
		self.assertEqual(COURSE["prerequisites"], "None")

	def test_module_contracts(self):
		week_titles = set()
		session_titles = set()
		for week_number, week in enumerate(WEEKS, start=1):
			self.assertNotIn(week["title"], week_titles)
			week_titles.add(week["title"])
			self.assertEqual(len(week["sessions"]), 1)
			self.assertEqual(len(week["quiz"]), 3)
			self.assertEqual(len(week["assignment"]), 3)

			for session_number, session in enumerate(week["sessions"], start=1):
				self.assertNotIn(session["title"], session_titles)
				session_titles.add(session["title"])
				self.assertEqual(len(session["outcomes"]), 3)
				self.assertEqual(len(session["concepts"]), 4)
				self.assertGreater(len(session["lab"]), 30)
				self.assertGreater(len(session["deliverable"]), 30)
				self.assertGreater(len(session["narration_en"]), 80)
				self.assertGreater(len(session["example"]["code"]), 40)
				self.assertGreaterEqual(len(session["example"]["output"]), 3)
				self.assertGreater(len(session["example"]["failure"]), 40)
				self.assertGreater(len(session["example"]["verify"]), 40)
				self.assertGreaterEqual(len(session["sources"]), 2)
				self.assertTrue(session["source_material"].startswith("https://"))
				self.assertGreater(len(session["modernization"]), 40)
				self.assertEqual(
					len(build_slide_outline(week_number, session_number, week, session)),
					12,
				)

			quiz_prompts = set()
			for prompt, options, correct_index in week["quiz"]:
				self.assertTrue(prompt.endswith("?"))
				self.assertNotIn(prompt, quiz_prompts)
				quiz_prompts.add(prompt)
				self.assertEqual(len(options), 4)
				self.assertEqual(len(set(options)), 4)
				self.assertIn(correct_index, range(len(options)))

			assignment_title, question, rubric = week["assignment"]
			self.assertGreater(len(assignment_title), 8)
			self.assertGreater(len(question), 60)
			self.assertIn("%", rubric)


if __name__ == "__main__":
	unittest.main()
