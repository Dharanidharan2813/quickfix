import frappe
from frappe.utils import now


def log_audit_entry(doc, method=None):
	if doc.doctype == "Audit Log":
		return
	else:
		if method == "on_update":
			action = "Updated"
		if method == "on_cancel":
			action = "Cancelled"
		if method == "on_submit":
			action = "Submitted"

		frappe.get_doc(
			{
				"doctype": "Audit Log",
				"doctype_name": doc.doctype,
				"document_name": doc.name,
				"action": action,
				"user": frappe.session.user,
				"timestamp": now(),
			}
		).insert()
		frappe.msgprint("Audit Log Created")
