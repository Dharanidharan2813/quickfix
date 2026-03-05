import frappe


@frappe.whitelist()
def get_job_card_details_unsafe():
	return frappe.get_all("Job Card", fields="*")


@frappe.whitelist()
def get_job_cards_safe():
	user = frappe.session.user
	job_cards = frappe.get_list(
		"Job Card",
		fields=["name", "customer", "status", "payment_status", "customer_phone", "customer_email"],
	)

	if "QF Manager" not in frappe.get_roles(user):
		for jc in job_cards:
			jc.pop("customer_phone", None)
			jc.pop("customer_email", None)

	return job_cards
