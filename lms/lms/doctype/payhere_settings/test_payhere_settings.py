from frappe.tests import UnitTestCase

from lms.lms.doctype.payhere_settings.payhere_settings import (
	add_query_parameter,
	format_amount,
	make_checkout_hash,
	make_notification_signature,
)


class TestPayHereSettings(UnitTestCase):
	def test_checkout_hash_matches_known_vector(self):
		self.assertEqual(
			make_checkout_hash(
				"1211149",
				"Order12345",
				"1000.00",
				"LKR",
				"MerchantSecret",
			),
			"47A0506493FE1AD213E2B7AE148C7BDB",
		)

	def test_notification_signature_matches_known_vector(self):
		self.assertEqual(
			make_notification_signature(
				"1211149",
				"Order12345",
				"1000.00",
				"LKR",
				"2",
				"MerchantSecret",
			),
			"AC70D1976337986A5653F8FE2CD74CB9",
		)

	def test_amount_is_always_two_decimal_places(self):
		self.assertEqual(format_amount("1250"), "1250.00")
		self.assertEqual(format_amount("19.995"), "20.00")

	def test_status_query_preserves_existing_query_string(self):
		self.assertEqual(
			add_query_parameter(
				"https://learn.dsacademy.lk/lms/courses/example?source=checkout",
				"payment_status",
				"processing",
			),
			"https://learn.dsacademy.lk/lms/courses/example?source=checkout&payment_status=processing",
		)
