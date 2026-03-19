import frappe
from frappe.utils import now


def after_install():
	deveice_type = ["Mobile", "Laptop", "Tablet"]

	for dt in deveice_type:
		if not frappe.db.exists("Device Type", dt):
			frappe.get_doc({"doctype": "Device Type", "device_type": dt}).insert(ignore_permissions=True)

	if not frappe.db.exixts("QuickFix Settings", "QuickFix Settings"):
		settings = frappe.get_doc(
			{
				"doctype": "QuickFix Settings",
				"shop_name": "QuickFix",
				"manager_email": "testduickfix@gamil.com",
				"default_labour_charge": 500,
				"low_stock_alert_enabled": 1,
			}
		)
		settings.insert(ignore_permissions=True)

	frappe.msgprint("QuickFix installed successfully with default setup.")


def before_uninstall():
	exists = frappe.db.exists("Job Card", {"docstatus": 1})
	if exists:
		frappe.throw("Cannot uninstall QuickFix: Submitted Job Cards exist. Please cancel them first.")


def extend_bootinfo(bootinfo):
	settings = frappe.get_single("QuickFix Settings")

	bootinfo.quickfix_shop_name = settings.shop_name
	bootinfo.quickfix_manager_email = settings.manager_email


def on_session_creation(login_manager):
	try:
		frappe.get_doc(
			{
				"doctype": "Audit Log",
				"document_type": "Session",
				"document_name": login_manager.user,
				"action": "Login",
				"user": login_manager.user,
				"timestamp": now(),
			}
		).insert(ignore_permissions=True)

	except Exception as e:
		frappe.log_error(str(e), "Session Creation Audit Failed")


def on_logout(login_manager):
	try:
		frappe.get_doc(
			{
				"doctype": "Audit Log",
				"document_type": "Session",
				"document_name": login_manager.user,
				"action": "Logout",
				"user": login_manager.user,
				"timestamp": frappe.utils.now(),
			}
		).insert(ignore_permissions=True)

	except Exception as e:
		frappe.log_error(str(e), "Logout Audit Failed")
