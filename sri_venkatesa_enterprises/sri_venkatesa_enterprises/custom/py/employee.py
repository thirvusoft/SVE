from erpnext.setup.doctype.employee.employee import Employee
import frappe
from frappe.model.naming import set_name_by_naming_series


class TsEmployeeName(Employee):
	def autoname(self):
		self.name = (self.first_name or "").strip() + " " + (self.last_name or "").strip()
		self.employee = self.name
