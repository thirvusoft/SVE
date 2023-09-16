# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime, nowdate

class EmployeeInOut(Document):
	def validate(self):
		if self.start_km and self.end_km and self.end_km < self.start_km:
			frappe.throw("End Km should be greater than Start Km")
	
	def after_insert(self):
		if frappe.db.exists("Employee In Out", {"attendance_date":nowdate(), "user":frappe.session.user}):
			frappe.throw(f"""Checkin Already created for Date: {now_datetime().strftime("%d-%m-%y")}""")
		self.db_set("attendance_date", nowdate())
		self.db_set("checkin_time", now_datetime())
		if(not self.user):
			self.db_set("user", frappe.session.user)
		self.reload()
		if self.user:
			emp = frappe.db.get_value("Employee", {"user_id":self.user, "status":["!=", "Inactive"]}, "name")
			self.db_set("employee", emp)
			if emp:
				sp = frappe.db.get_value("Sales Person", {"employee":emp, "enabled":1}, "name")
				self.db_set("sales_person", sp)


@frappe.whitelist()
def create_checkin(start_km=0):
	doc=frappe.new_doc("Employee In Out")
	doc.update({
		"start_km":start_km
	})
	doc.insert()
	return doc

@frappe.whitelist()
def validate_checkout():
	if not frappe.db.exists("Employee In Out", {"attendance_date":nowdate(), "user":frappe.session.user}):
		frappe.throw(f"""Checkin not Found for Date: {now_datetime().strftime("%d-%m-%y")}""")
	doc = frappe.get_last_doc("Employee In Out", {"attendance_date":nowdate(), "user":frappe.session.user})
	if doc.get("checkout_time"):
		frappe.throw("Checkout already created")
	return True

@frappe.whitelist()
def create_checkout(end_km=0, total_km=0):
	doc = frappe.get_last_doc("Employee In Out", {"attendance_date":nowdate(), "user":frappe.session.user})
	if doc.get("checkout_time"):
		frappe.throw("Checkout already created")
	doc.update({
		"end_km":float(end_km),
		"total_distance":float(total_km),
		"checkout_time":now_datetime()
	})
	doc.save()
	return doc