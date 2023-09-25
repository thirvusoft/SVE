# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import sri_venkatesa_enterprises as sve
from frappe.model.document import Document

class DailyActivity(Document):
	@frappe.whitelist()
	def get_employee_id(self):
		self.employee = sve.get_user_details().employee
