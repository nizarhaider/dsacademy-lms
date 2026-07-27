"""Contract tests for the versioned DS Academy curriculum."""

import unittest

from lms.dsacademy.curriculum import COURSE, WEEKS


class CurriculumContractTest(unittest.TestCase):
	def test_program_shape(self):
		self.assertEqual(len(WEEKS), 12)
		self.assertEqual(sum(len(week["sessions"]) for week in WEEKS), 24)
		self.assertEqual(sum(len(week["quiz"]) for week in WEEKS), 36)
		self.assertEqual(COURSE["title"], "End-to-End Data Science & AI")
		self.assertIn("English", COURSE["description"])
		self.assertIn("Sinhala", COURSE["description"])

	def test_week_contracts(self):
		week_titles = set()
		session_titles = set()
		for week in WEEKS:
			self.assertNotIn(week["title"], week_titles)
			week_titles.add(week["title"])
			self.assertEqual(len(week["sessions"]), 2)
			self.assertEqual(len(week["quiz"]), 3)
			self.assertEqual(len(week["assignment"]), 3)

			for session in week["sessions"]:
				self.assertNotIn(session["title"], session_titles)
				session_titles.add(session["title"])
				self.assertEqual(len(session["outcomes"]), 3)
				self.assertEqual(len(session["concepts"]), 4)
				self.assertGreater(len(session["lab"]), 30)
				self.assertGreater(len(session["deliverable"]), 30)
				self.assertGreater(len(session["narration_en"]), 80)
				self.assertGreater(len(session["narration_si"]), 80)
				self.assertRegex(session["narration_si"], r"[\u0D80-\u0DFF]")

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
