# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import sri_venkatesa_enterprises as sve
from frappe.model.document import Document

class DailyActivity(Document):
	def autoname(self):
		self.name = f"{self.employee}-{self.get_formatted('date')}"

	@frappe.whitelist()
	def get_employee_id(self):
		if self.get("__islocal"):
			self.employee = sve.get_user_details().employee
	
	def validate(self):
		self.set_customer_details()

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
		else:
			for row in self.for_customer:
				if row.customer:
					row.batch_size = sum(frappe.db.get_list('Farm Details', {'customer': row.customer}, pluck = 'chick_capacity__laying'))

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
