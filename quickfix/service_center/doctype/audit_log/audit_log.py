# Copyright (c) 2026, dharanidharans and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class AuditLog(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		action: DF.Literal["Updated", "Cancelled", "Submitted"]
		doctype_name: DF.Data | None
		document_name: DF.Data | None
		timestamp: DF.Datetime | None
		user: DF.Link | None
	# end: auto-generated types

	pass
