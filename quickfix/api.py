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


def send_job_ready_email(job, user):
	job_doc = frappe.get_doc("Job Card", job)

	frappe.sendmail(
		print(f"Sending email for job {job} to user {user}"),
		recipients=[frappe.db.get_value("User", user, "email")],
		subject=f"Job {job_doc.name} is Ready",
		message=f"The job {job_doc.name} has been completed and is ready.",
	)
