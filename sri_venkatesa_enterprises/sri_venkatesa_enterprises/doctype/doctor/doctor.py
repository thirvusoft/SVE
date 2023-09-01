# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact

class Doctor(Document):
	def onload(self):
		if not self.is_new():
			load_address_and_contact(self)
	
	def validate(self):
		self.flags.is_new_doc = self.is_new() or frappe.flags.in_import

	def on_update(self):
		if self.flags.is_new_doc and self.get("mobile_no"):
			self.make_contact()

	def make_contact(self):
		contact = frappe.get_doc(
			{
				"doctype": "Contact",
				"first_name": self.doctor_name,
				"is_primary_contact": 1,
				"links": [{"link_doctype": self.get("doctype"), "link_name": self.get("name")}],
			}
		)
		if self.get("email_id"):
			contact.add_email(self.get("email_id"), is_primary=True)
		if self.get("mobile_no"):
			contact.add_phone(self.get("mobile_no"), is_primary_mobile_no=True)
		contact.insert()

		return contact