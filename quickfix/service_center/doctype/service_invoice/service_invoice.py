# Copyright (c) 2026, dharanidharans and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		invoice_date: DF.Date | None
		job_card: DF.Link
		labour_charge: DF.Currency
		name1: DF.Data | None
		naming_series: DF.Literal["INV-.YYYY.-.#####"]
		parts_total: DF.Currency
		payment_status: DF.Literal["Unpaid", "Paid"]
		total_amount: DF.Currency
	# end: auto-generated types

	pass


def has_permission(doc, user):
	if not user:
		user = frappe.session.user
	if "Manager" in frappe.get_roles(user):
		return True

	if not doc.job_card:
		return False

	payment_status = frappe.db.get_value("Job Card", doc.job_card, "payment_status")

	if payment_status != "Paid":
		return False

	return True
