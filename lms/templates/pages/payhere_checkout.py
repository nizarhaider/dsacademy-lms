import frappe
from frappe import _

from lms.lms.doctype.payhere_settings.payhere_settings import get_checkout_context


def get_context(context):
	context.no_cache = 1
	try:
		context.update(get_checkout_context(frappe.form_dict.get("payment")))
	except Exception:
		frappe.log_error(title="PayHere Checkout Error")
		frappe.redirect_to_message(
			_("Unable to start payment"),
			_("The payment link is invalid or the PayHere gateway is not configured."),
			http_status_code=400,
			indicator_color="red",
		)
		frappe.local.flags.redirect_location = frappe.local.response.location
		raise frappe.Redirect
