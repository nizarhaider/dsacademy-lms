import hashlib
import hmac
from decimal import ROUND_HALF_UP, Decimal, InvalidOperation
from urllib.parse import urlencode

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, get_url

from lms.lms.payments import get_redirect_url
from lms.lms.utils import complete_enrollment

PAYHERE_LIVE_URL = "https://www.payhere.lk/pay/checkout"
PAYHERE_SANDBOX_URL = "https://sandbox.payhere.lk/pay/checkout"
SUPPORTED_CURRENCIES = ("LKR", "USD")
SUCCESS_STATUS = "2"


class PayHereSettings(Document):
	supported_currencies = SUPPORTED_CURRENCIES

	def validate(self):
		ensure_payhere_gateway()
		if cint(self.enabled):
			self.validate_checkout()

	def validate_checkout(self):
		if not cint(self.enabled):
			frappe.throw(_("PayHere is not enabled."))
		if not self.merchant_id:
			frappe.throw(_("PayHere Merchant ID is required when the gateway is enabled."))
		if not self.get_password("merchant_secret", raise_exception=False):
			frappe.throw(_("PayHere Merchant Secret is required when the gateway is enabled."))

	def validate_transaction_currency(self, currency):
		if currency not in self.supported_currencies:
			frappe.throw(
				_("PayHere does not support transactions in currency {0}.").format(frappe.bold(currency))
			)

	def get_payment_url(self, **kwargs):
		self.validate_checkout()
		self.validate_transaction_currency(kwargs.get("currency"))
		payment = kwargs.get("payment")
		if not payment:
			frappe.throw(_("A valid LMS payment reference is required."))
		return get_url(f"/payhere_checkout?{urlencode({'payment': payment})}")


def ensure_payhere_gateway():
	if "payments" not in frappe.get_installed_apps():
		return

	from payments.utils import create_payment_gateway

	create_payment_gateway("PayHere")


def format_amount(amount) -> str:
	try:
		value = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
	except (InvalidOperation, TypeError, ValueError):
		frappe.throw(_("Invalid PayHere payment amount."))
	if value <= 0:
		frappe.throw(_("PayHere payment amount must be greater than zero."))
	return f"{value:.2f}"


def md5_upper(value: str) -> str:
	return hashlib.md5(value.encode("utf-8")).hexdigest().upper()


def make_checkout_hash(
	merchant_id: str,
	order_id: str,
	amount: str,
	currency: str,
	merchant_secret: str,
) -> str:
	hashed_secret = md5_upper(merchant_secret)
	return md5_upper(f"{merchant_id}{order_id}{amount}{currency}{hashed_secret}")


def make_notification_signature(
	merchant_id: str,
	order_id: str,
	amount: str,
	currency: str,
	status_code: str,
	merchant_secret: str,
) -> str:
	hashed_secret = md5_upper(merchant_secret)
	return md5_upper(f"{merchant_id}{order_id}{amount}{currency}{status_code}{hashed_secret}")


def get_checkout_context(payment_name: str) -> dict:
	if frappe.session.user == "Guest":
		frappe.throw(_("Please sign in before starting a payment."), frappe.PermissionError)

	settings = frappe.get_single("PayHere Settings")
	settings.validate_checkout()

	payment = frappe.get_doc("LMS Payment", payment_name)
	if payment.member != frappe.session.user:
		frappe.throw(_("You cannot access this payment."), frappe.PermissionError)
	if payment.payment_received:
		frappe.throw(_("This payment has already been completed."))

	settings.validate_transaction_currency(payment.currency)
	address = frappe.get_doc("Address", payment.address)
	user = frappe.get_doc("User", payment.member)
	amount = format_amount(payment.amount_with_gst or payment.amount)
	redirect_url = get_redirect_url(
		payment.payment_for_document_type,
		payment.payment_for_document,
		payment.payment_for_certificate,
	)
	order_id = payment.name

	first_name, last_name = get_customer_name(user, payment.billing_name)
	required_customer_fields = {
		"first_name": first_name,
		"last_name": last_name,
		"email": payment.member,
		"phone": address.phone,
		"address": " ".join(part for part in (address.address_line1, address.address_line2) if part),
		"city": address.city,
		"country": address.country,
	}
	missing = [label for label, value in required_customer_fields.items() if not value]
	if missing:
		frappe.throw(_("Complete these billing fields before paying: {0}.").format(", ".join(missing)))

	merchant_secret = settings.get_password("merchant_secret")
	checkout_fields = {
		"merchant_id": settings.merchant_id,
		"return_url": add_query_parameter(get_url(redirect_url), "payment_status", "processing"),
		"cancel_url": add_query_parameter(get_url(redirect_url), "payment_status", "cancelled"),
		"notify_url": get_url("/api/method/lms.lms.doctype.payhere_settings.payhere_settings.notify"),
		"order_id": order_id,
		"items": get_payment_title(payment),
		"currency": payment.currency,
		"amount": amount,
		"hash": make_checkout_hash(
			settings.merchant_id,
			order_id,
			amount,
			payment.currency,
			merchant_secret,
		),
		**required_customer_fields,
	}
	frappe.db.set_value("LMS Payment", payment.name, "order_id", order_id)

	return {
		"checkout_url": PAYHERE_SANDBOX_URL if cint(settings.sandbox) else PAYHERE_LIVE_URL,
		"payment_details": checkout_fields,
	}


def get_customer_name(user, billing_name: str) -> tuple[str, str]:
	first_name = (user.first_name or "").strip()
	last_name = (user.last_name or "").strip()
	if first_name and last_name:
		return first_name, last_name

	parts = (billing_name or user.full_name or "").strip().split(maxsplit=1)
	return (parts[0] if parts else "", parts[1] if len(parts) > 1 else "-")


def get_payment_title(payment) -> str:
	title = frappe.db.get_value(
		payment.payment_for_document_type,
		payment.payment_for_document,
		"title",
	)
	return str(title or payment.payment_for_document)[:150]


def add_query_parameter(url: str, key: str, value: str) -> str:
	separator = "&" if "?" in url else "?"
	return f"{url}{separator}{urlencode({key: value})}"


@frappe.whitelist(allow_guest=True)
def notify():
	if frappe.request and frappe.request.method != "POST":
		frappe.throw(_("PayHere notifications must use POST."), frappe.PermissionError)

	data = frappe._dict(frappe.local.form_dict)
	data.pop("cmd", None)
	required = (
		"merchant_id",
		"order_id",
		"payment_id",
		"payhere_amount",
		"payhere_currency",
		"status_code",
		"md5sig",
	)
	if any(not data.get(field) for field in required):
		frappe.throw(_("Incomplete PayHere notification."))

	settings = frappe.get_single("PayHere Settings")
	settings.validate_checkout()
	merchant_secret = settings.get_password("merchant_secret")
	expected_signature = make_notification_signature(
		data.merchant_id,
		data.order_id,
		data.payhere_amount,
		data.payhere_currency,
		data.status_code,
		merchant_secret,
	)
	if not hmac.compare_digest(str(data.merchant_id), str(settings.merchant_id)):
		frappe.throw(_("Invalid PayHere merchant."), frappe.PermissionError)
	if not hmac.compare_digest(str(data.md5sig).upper(), expected_signature):
		frappe.throw(_("Invalid PayHere signature."), frappe.PermissionError)

	payment = lock_payment(data.order_id)
	validate_notification_payment(payment, data)

	if data.status_code == SUCCESS_STATUS and not payment.payment_received:
		complete_payhere_payment(payment, data.payment_id)
	elif data.status_code == "-3":
		frappe.log_error(
			message=f"PayHere chargeback received for LMS Payment {payment.name}.",
			title="PayHere Chargeback",
		)
	elif data.status_code != SUCCESS_STATUS and not payment.payment_received:
		frappe.db.set_value(
			"LMS Payment",
			payment.name,
			{"order_id": data.order_id, "payment_id": data.payment_id},
		)

	return "OK"


def lock_payment(order_id: str):
	rows = frappe.db.sql(
		"""
		SELECT
			name, member, payment_received, amount, amount_with_gst, currency,
			payment_for_document_type, payment_for_document, payment_for_certificate
		FROM `tabLMS Payment`
		WHERE name = %s
		FOR UPDATE
		""",
		order_id,
		as_dict=True,
	)
	if not rows:
		frappe.throw(_("Unknown PayHere order."))
	return frappe._dict(rows[0])


def validate_notification_payment(payment, data):
	expected_amount = format_amount(payment.amount_with_gst or payment.amount)
	try:
		notified_amount = format_amount(data.payhere_amount)
	except frappe.ValidationError:
		frappe.throw(_("Invalid PayHere notification amount."))

	if not hmac.compare_digest(expected_amount, notified_amount):
		frappe.throw(_("PayHere payment amount does not match the order."))
	if not hmac.compare_digest(str(payment.currency), str(data.payhere_currency)):
		frappe.throw(_("PayHere payment currency does not match the order."))


def complete_payhere_payment(payment, payment_id: str):
	original_user = frappe.session.user
	try:
		frappe.set_user(payment.member)
		complete_enrollment(
			payment.name,
			payment.payment_for_document_type,
			payment.payment_for_document,
		)
		frappe.db.set_value(
			"LMS Payment",
			payment.name,
			{
				"payment_received": 1,
				"payment_id": payment_id,
				"order_id": payment.name,
			},
		)
	finally:
		frappe.set_user(original_user)
