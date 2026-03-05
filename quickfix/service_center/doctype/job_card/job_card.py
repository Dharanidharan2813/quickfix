# Copyright (c) 2026, dharanidharans and contributors
# For license information, please see license.txt

import re

import frappe
from frappe.model.document import Document


class JobCard(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		from quickfix.service_center.doctype.part_usage_entry.part_usage_entry import PartUsageEntry

		amended_from: DF.Link | None
		assigned_technician: DF.Link | None
		customer_email: DF.Data | None
		customer_name: DF.Data
		customer_phone: DF.Data
		delivery_date: DF.Date | None
		device_brand: DF.Data | None
		device_model: DF.Data | None
		device_type: DF.Link
		diagnosis_date: DF.Data | None
		diagnosis_notes: DF.TextEditor | None
		estimated_cost: DF.Currency
		final_amount: DF.Currency
		imei_or_serial: DF.Data | None
		labour_charge: DF.Currency
		parts_total: DF.Currency
		parts_used: DF.Table[PartUsageEntry]
		payment_status: DF.Literal["Unpaid", "Paid"]
		priority: DF.Literal["Normal", "HighUrgent, default Normal"]
		problem_description: DF.TextEditor
		remarks: DF.SmallText | None
		status: DF.Literal[
			"Draft",
			"Pending Diagnosis",
			"Awaiting Customer Approval",
			"In Repair",
			"Ready for Delivery",
			"Delivered",
			"Cancelled",
		]
	# end: auto-generated types

	def validate(self):
		self.validate_phone_number()
		self.assigin_technician()
		self.validate_item_total()
		self.get_labour_charge()
		self.final_amount_calculation()

	def before_submit(self):
		self.check_status()
		self.check_stock_quantity()

	def on_submit(self):
		# self.deduct_stock()
		# self.auto_create_service_invoice()
		self.show_realtime()

	def on_cancel(self):
		self.set_status_cancelled()
		self.restore_stock()
		self.cancel_linked_invoice()

	def on_trash(self):
		print("Attempting to delete Job Card:", self.name)
		self.prevent_deletion()

	def on_update(self):
		pass

	# validation methods

	def validate_phone_number(self):
		pattern = r"^[6-9]\d{9}$"
		if self.customer_phone and not re.match(pattern, self.customer_phone):
			frappe.throw("Invalid phone number. It should be a 10-digit number starting with 6-9.")

	def assigin_technician(self):
		if self.status in ["In Repair", "Ready for Delivery", "Delivered"] and not self.assigned_technician:
			frappe.throw(f"Technician must be assigned when the job card is in {self.status} status.")

	def validate_item_total(self):
		total = 0
		for row in self.parts_used:
			row.total_price = row.quantity * row.unit_price
			total += row.total_price
		self.parts_total = total

	def get_labour_charge(self):
		if self.labour_charge == 0:
			self.labour_charge = frappe.db.get_single_value("Quickfix Settings", "default_labour_charge")

	def final_amount_calculation(self):
		self.final_amount = self.parts_total + self.labour_charge

	# before submit methods

	def check_status(self):
		if self.status != "Ready for Delivery":
			frappe.throw("Job Card can only be submitted when the status is 'Ready for Delivery'.")

	def check_stock_quantity(self):
		for row in self.parts_used:
			avaliable_quantity = frappe.db.get_value("Spare Part", row.part, "stock_qty")
			if row.quantity > avaliable_quantity:
				frappe.throw(f"Not enough stock for {row.part}. Available quantity: {avaliable_quantity}.")

	# on submit methods

	def deduct_stock(self):
		for row in self.parts_used:
			avaliable_stock = frappe.db.get_value("Spare Part", row.part, "stock_qty")
			new_stock = avaliable_stock - row.quantity
			frappe.db.set_value("Spare Part", row.part, "stock_qty", new_stock)

	def auto_create_service_invoice(self):
		if self.payment_status == "Unpaid" and self.status == "Ready for Delivery":
			invoice = frappe.get_doc(
				{
					"doctype": "Service Invoice",
					"job_card": self.name,
					"invoice_date": self.delivery_date,
					"labour_charge": self.labour_charge,
					"parts_total": self.parts_total,
					"total_amount": self.final_amount,
					"payment_status": self.payment_status,
				}
			)
			invoice.insert()
			invoice.submit()
			frappe.msgprint("Service Invoice created and submitted successfully.")

	def show_realtime(self):
		frappe.enqueue(
			"quickfix.quickfix.api.send_job_ready_email", queue="short", job=self.name, user=self.owner
		)
		frappe.publish_realtime(
			"job_ready",
			{
				"job": self.name,
				"status": "Ready",
			},
			user=self.owner,
		)

	# on cancel methods

	def set_status_cancelled(self):
		self.status = "Cancelled"

	def restore_stock(self):
		for row in self.parts_used:
			current_stock = frappe.db.get_value("Spare Part", row.part, "stock_qty")
			new_stock = current_stock + row.quantity
			frappe.db.set_value("Spare Part", row.part, "stock_qty", new_stock)

	def cancel_linked_invoice(self):
		invoice_name = frappe.db.get_value("Service Invoice", {"job_card": self.name}, "name")
		if invoice_name:
			invoice_doc = frappe.get_doc("Service Invoice", invoice_name)
			if invoice_doc.docstatus == 1:
				invoice_doc.cancel()

	# on trash methods

	def prevent_deletion(self):
		print(f"Attempting to delete Job Card: {self.name} with status {self.status}")
		if self.status != "Draft" and self.status != "Cancelled":
			frappe.throw("Only Job Cards in Draft or Cancelled status can be deleted.")
