# Copyright (c) 2026, dharanidharans and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Technician(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		email: DF.Data | None
		employee_id: DF.Data | None
		joining_date: DF.Date | None
		notes: DF.Text | None
		phone: DF.Data | None
		photo: DF.Attach | None
		specialization: DF.Link | None
		status: DF.Literal["Active", "On Leave", "Resigned"]
		technician_name: DF.Data
		user: DF.Link | None
	# end: auto-generated types

	pass
