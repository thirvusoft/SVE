# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.address_and_contact import load_address_and_contact

class Doctor(Document):
	def onload(self):
		if not self.is_new():
			load_address_and_contact(self)
