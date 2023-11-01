# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import sri_venkatesa_enterprises as sve
from frappe.model.document import Document

class DailyActivity(Document):
	def autoname(self):
		abbr = frappe.db.get_value("Territory", {"name":self.route}, "custom_territory_abbr")
		self.name = f"{abbr}-{self.employee}-{self.get_formatted('date')}"

	@frappe.whitelist()
	def get_employee_id(self):
		if self.get("__islocal"):
			self.employee = sve.get_user_details().employee
	
	def validate(self):
		self.set_customer_details()
		self.update_todo_for_appointments()

	def on_update(self):
		self.create_todo_for_appointments()
		self.reload()
	
	def after_delete(self):
		self.delete_todo(delete_all=True)

	def set_customer_details(self):
		if self.date:
			for row in self.for_customer:
				if row.customer:
					row.batch_size = sum(frappe.db.get_list('Farm Details', {'customer': row.customer}, pluck = 'chick_capacity__laying'))
					value = get_customer_order_ids_and_values(row.customer, self.date)
					row.order_id = value.get('ids') or ''
					row.order_value = value.get('values') or 0
					row.outstanding = value.get('outstanding_amount') or 0
					row.collection_value = value.get('paid_amount') or 0
				
			for row in self.for_doctor_and_dealer:
				if row.customer:
					value = get_customer_order_ids_and_values(row.customer, self.date)
					row.order_id = value.get('ids') or ''
					row.order_value = value.get('values') or 0
					row.outstanding = value.get('outstanding_amount') or 0
					row.collection_value = value.get('paid_amount') or 0
			for row in self.appointments:
				if row.customer and row.get('__islocal'):
					value = get_customer_order_ids_and_values(row.customer, self.date)
					row.outstanding_amount = value.get('outstanding_amount') or 0
					row.collection_value = value.get('paid_amount') or 0
				elif row.customer:
					value = get_customer_order_ids_and_values(row.customer, self.date)
					row.collection_value = value.get('paid_amount') or 0
		else:
			for row in self.for_customer:
				if row.customer:
					row.batch_size = sum(frappe.db.get_list('Farm Details', {'customer': row.customer}, pluck = 'chick_capacity__laying'))
	
	def update_todo_for_appointments(self):
		self.delete_todo()

	def delete_todo(self, delete_all=None):
		if not self.get('__islocal'):
			appointment_row_names = [row.name for row in self.appointments]
			for_customer_row_names = [row.name for row in self.for_customer]
			for_doctor_row_names = [row.name for row in self.for_doctor_and_dealer]
			old_doc = self.get_doc_before_save() or (self if delete_all else frappe._dict())
			for row in old_doc.get('appointments') or []:
				if row.name not in appointment_row_names or delete_all:
					if row.appointment_todo:
						appointment_todo = row.appointment_todo
						row.db_set('appointment_todo', '')
						frappe.delete_doc('ToDo', appointment_todo)
					if row.payment_todo:
						payment_todo = row.payment_todo
						row.db_set('payment_todo', '')
						frappe.delete_doc('ToDo', payment_todo)
					
					if row.appointment_notification_log:
						appointment_notification_log = row.appointment_notification_log
						row.db_set('appointment_notification_log', '')
						frappe.delete_doc('Notification Log', appointment_notification_log)
					if row.payment_notification_log:
						payment_notification_log = row.payment_notification_log
						row.db_set('payment_notification_log', '')
						frappe.delete_doc('Notification Log', payment_notification_log)

			for row in old_doc.get('for_customer') or []:
				if row.name not in for_customer_row_names or delete_all:
					if row.todo:
						todo = row.todo
						row.db_set('todo', '')
						frappe.delete_doc('ToDo', todo)
			for row in old_doc.get('for_doctor_and_dealer') or []:
				if row.name not in for_doctor_row_names or delete_all:
					if row.todo:
						todo = row.todo
						row.db_set('todo', '')
						frappe.delete_doc('ToDo', todo)
		
		for row in self.appointments:
			if not row.appointment_date:
				appointment_todo, appointment_notification_log = row.appointment_todo, row.appointment_notification_log
				row.db_set('appointment_todo', '')
				row.db_set('appointment_notification_log', '')
				frappe.delete_doc('ToDo', appointment_todo)
				frappe.delete_doc('Notification Log', appointment_notification_log)
			
			if not row.payment_date:
				payment_todo, payment_notification_log = row.payment_todo, row.payment_notification_log
				row.db_set('payment_todo', '')
				row.db_set('payment_notification_log', '')
				frappe.delete_doc('ToDo', payment_todo)
				frappe.delete_doc('Notification Log', payment_notification_log)

		for row in self.for_customer:
			if not row.next_follow_up:
				todo = row.todo
				row.db_set('todo', '')
				frappe.delete_doc('ToDo', todo)

		for row in self.for_doctor_and_dealer:
			if not row.next_follow_up:
				todo = row.todo
				row.db_set('todo', '')
				frappe.delete_doc('ToDo', todo)

	def create_todo_for_appointments(self):
		employee_user = (frappe.db.get_value("Employee", self.employee, 'user_id') or '') if self.employee else ''
		for row in self.appointments:
			if row.appointment_date:
				if row.appointment_todo:
					appointment_todo_doc = frappe.get_doc("ToDo", row.appointment_todo)
				else:
					appointment_todo_doc = frappe.new_doc("ToDo")
				appointment_todo_doc.update({
					'description': f"""Assignemnt for Appointment followup for {row.customer} at {row.get_formatted('appointment_date')} in {self.doctype} {self.name}""",
					'allocated_to': employee_user,
					'date': row.appointment_date,
					'reference_type': self.doctype,
					'reference_name': self.name
				})
				appointment_todo_doc.save()
				row.db_set('appointment_todo', appointment_todo_doc.name)

				if row.appointment_notification_log:
					appointment_notification_log_doc = frappe.get_doc("Notification Log", row.appointment_notification_log)
				else:
					appointment_notification_log_doc = frappe.new_doc("Notification Log")
				appointment_notification_log_doc.update({
					"subject": f"""Assignemnt for Appointment followup for {row.customer} at {row.get_formatted('appointment_date')} in {self.doctype} {self.name}""",
					"for_user": employee_user,
					"type": "Assignment",
					"email_content": f"""Assignemnt for Appointment followup for {row.customer} at {row.get_formatted('appointment_date')} in {self.doctype} {self.name}""",
					"document_type": self.doctype,
					"document_name": self.name,
				})
				appointment_notification_log_doc.save()
				row.db_set('appointment_notification_log', appointment_notification_log_doc.name)
			
			if row.payment_date:
				if row.payment_todo:
					payment_todo_doc = frappe.get_doc("ToDo", row.payment_todo)
				else:
					payment_todo_doc = frappe.new_doc("ToDo")
				payment_todo_doc.update({
					'description': f"""Assignemnt for Payment followup for {row.customer} at {row.get_formatted('payment_date')} in {self.doctype} {self.name}""",
					'allocated_to': employee_user,
					'date': row.payment_date,
					'reference_type': self.doctype,
					'reference_name': self.name
				})
				payment_todo_doc.save()
				row.db_set('payment_todo', payment_todo_doc.name)

				if row.payment_notification_log:
					payment_notification_log_doc = frappe.get_doc("Notification Log", row.payment_notification_log)
				else:
					payment_notification_log_doc = frappe.new_doc("Notification Log")
				payment_notification_log_doc.update({
					"subject": f"""Assignemnt for Payment followup for {row.customer} at {row.get_formatted('payment_date')} in {self.doctype} {self.name}""",
					"for_user": employee_user,
					"type": "Assignment",
					"email_content": f"""Assignemnt for Payment followup for {row.customer} at {row.get_formatted('payment_date')} in {self.doctype} {self.name}""",
					"document_type": self.doctype,
					"document_name": self.name,
				})
				payment_notification_log_doc.save()
				row.db_set('payment_notification_log', payment_notification_log_doc.name)

		for row in self.for_customer:
			if row.next_follow_up:
				if row.todo:
					appointment_todo_doc = frappe.get_doc("ToDo", row.todo)
				else:
					appointment_todo_doc = frappe.new_doc("ToDo")
				appointment_todo_doc.update({
					'description': f"""Assignemnt for Next followup for {row.customer} at {row.get_formatted('next_follow_up')} in {self.doctype} {self.name}""",
					'allocated_to': employee_user,
					'date': row.next_follow_up,
					'reference_type': self.doctype,
					'reference_name': self.name
				})
				appointment_todo_doc.save()
				row.db_set('todo', appointment_todo_doc.name)

		for row in self.for_doctor_and_dealer:
			if row.next_follow_up:
				if row.todo:
					appointment_todo_doc = frappe.get_doc("ToDo", row.todo)
				else:
					appointment_todo_doc = frappe.new_doc("ToDo")
				appointment_todo_doc.update({
					'description': f"""Assignemnt for Next Doctor/Dealer followup for {row.customer} at {row.get_formatted('next_follow_up')} in {self.doctype} {self.name}""",
					'allocated_to': employee_user,
					'date': row.next_follow_up,
					'reference_type': self.doctype,
					'reference_name': self.name
				})
				appointment_todo_doc.save()
				row.db_set('todo', appointment_todo_doc.name)
		

@frappe.whitelist()
def get_customer_order_ids_and_values(customer, date):
	return {
		"ids": ", ".join(frappe.db.get_all("Sales Order", {'docstatus': ['!=', 2], 'customer': customer, 'transaction_date': date}, pluck="name")),
		"values": sum(frappe.db.get_all("Sales Order", {'docstatus': ['!=', 2], 'customer': customer, 'transaction_date': date}, pluck="rounded_total")),
		"outstanding_amount": (oa_res[0][0] if (oa_res:=frappe.db.sql("""
				SELECT
					SUM(gl.debit) - SUM(gl.credit)
				FROM `tabGL Entry` gl
				WHERE
					gl.is_cancelled = 0 AND
					gl.party_type = 'Customer' AND
					gl.party = %(customer)s	AND
					gl.posting_date <= %(date)s
			""", {
				"customer": customer,
				"date": date
			})) and oa_res[0] and oa_res[0][0] else 0),
		"paid_amount": (pa_res[0][0] if (pa_res:=frappe.db.sql("""
			SELECT
				SUM(gl.credit)
			FROM `tabGL Entry` gl
			WHERE
				gl.is_cancelled = 0 AND
				gl.party_type = 'Customer' AND
				gl.party = %(customer)s	AND
				gl.posting_date = %(date)s
		""", {
			"customer": customer,
			"date": date
		})) and pa_res[0] and pa_res[0][0] else 0)
	}

def update_outstanding_amount(self, event=None):
	if self.party_type == "Customer":
		date = self.posting_date
		for row in frappe.db.get_all('Daily Activity',
   				   [['Daily Activity', 'date', '>=', date], ['Customer Daily Activity', 'customer', '=', self.party]],
   				   ["`tabCustomer Daily Activity`.name, `tabCustomer Daily Activity`.customer, `tabDaily Activity`.date"]):
			value = get_customer_order_ids_and_values(row.customer, row.date)
			frappe.db.set_value('Customer Daily Activity', row.name, 'order_id', value.get('ids') or '')
			frappe.db.set_value('Customer Daily Activity', row.name, 'order_value', value.get('values') or 0)
			frappe.db.set_value('Customer Daily Activity', row.name, 'outstanding', value.get('outstanding_amount') or 0)
			frappe.db.set_value('Customer Daily Activity', row.name, 'collection_value', value.get('paid_amount') or 0)

		for row in frappe.db.get_all('Daily Activity',
   				   [['Daily Activity', 'date', '>=', date], ['Doctor Dealer Daily Activity', 'customer', '=', self.party]],
   				   ["`tabDoctor Dealer Daily Activity`.name, `tabDoctor Dealer Daily Activity`.customer, `tabDaily Activity`.date"]):
			value = get_customer_order_ids_and_values(row.customer, row.date)
			frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'order_id', value.get('ids') or '')
			frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'order_value', value.get('values') or 0)
			frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'outstanding', value.get('outstanding_amount') or 0)
			frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'collection_value', value.get('paid_amount') or 0)

		for row in frappe.db.get_all('Daily Activity',
   				   [['Daily Activity', 'date', '=', date], ['Daily Activity Appointments', 'customer', '=', self.party]],
   				   ["`tabDaily Activity Appointments`.name, `tabDaily Activity Appointments`.customer, `tabDaily Activity`.date"]):
			value = get_customer_order_ids_and_values(row.customer, row.date)
			frappe.db.set_value('Daily Activity Appointments', row.name, 'collection_value', value.get('paid_amount') or 0)

def update_order_details(self, event=None):
	date = self.transaction_date
	for row in frappe.db.get_all('Daily Activity',
   				   [['Daily Activity', 'date', '=', date], ['Customer Daily Activity', 'customer', '=', self.customer]],
   				   ["`tabCustomer Daily Activity`.name, `tabCustomer Daily Activity`.customer, `tabDaily Activity`.date"]):
		value = get_customer_order_ids_and_values(row.customer, row.date)
		frappe.db.set_value('Customer Daily Activity', row.name, 'order_id', value.get('ids') or '')
		frappe.db.set_value('Customer Daily Activity', row.name, 'order_value', value.get('values') or 0)
		frappe.db.set_value('Customer Daily Activity', row.name, 'outstanding', value.get('outstanding_amount') or 0)
		frappe.db.set_value('Customer Daily Activity', row.name, 'collection_value', value.get('paid_amount') or 0)
	
	for row in frappe.db.get_all('Daily Activity',
   				   [['Daily Activity', 'date', '=', date], ['Doctor Dealer Daily Activity', 'customer', '=', self.customer]],
   				   ["`tabDoctor Dealer Daily Activity`.name, `tabDoctor Dealer Daily Activity`.customer, `tabDaily Activity`.date"]):
		value = get_customer_order_ids_and_values(row.customer, row.date)
		frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'order_id', value.get('ids') or '')
		frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'order_value', value.get('values') or 0)
		frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'outstanding', value.get('outstanding_amount') or 0)
		frappe.db.set_value('Doctor Dealer Daily Activity', row.name, 'collection_value', value.get('paid_amount') or 0)
