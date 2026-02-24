# Copyright (c) 2026, dharanidharans and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class ServiceInvoice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		amended_from: DF.Link | None
		invoice_date: DF.Date | None
		invoice_number: DF.Literal["INV-.YYYY.-.#####"]
		job_card: DF.Link
		labour_charge: DF.Currency
		name1: DF.Data | None
		parts_total: DF.Currency
		payment_status: DF.Literal["Unpaid", "Paid"]
		total_amount: DF.Currency
	# end: auto-generated types

	pass
