# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data
def get_columns():
	columns = [
		{
			"fieldname":"invoice_no",
			"label":"Sales/Purchase Invoice No",
			"fieldtype":"Data",
			"width":150
		},
		{
			"fieldname":"invoiced_value",
			"label":"Invoiced value",
			"fieldtype":"Currency",
			"width":150
		},
		{
			"fieldname":"transporter",
			"label":"Transporter Details",
			"fieldtype":"Link",
			"options":"Supplier",
			"width":150
		},
		{
			"fieldname":"transport_charge",
			"label":"Transport Charge",
			"fieldtype":"Currency",
			"width":150
		},
		{
			"fieldname":"auto_charge",
			"label":"Auto Charge",
			"fieldtype":"Currency",
			"width":150
		},
	]
	return columns

def get_data(filters):
	data = []
	if not filters.get("voucher_type") or filters.get("voucher_type") == "Sales Invoice":
		si_conditions={"docstatus":1}
		if filters.get("from_date") and filters.get("to_date"):
			si_conditions.update({"posting_date":["between", [filters.get("from_date"), filters.get("to_date")]]})
		if filters.get("transporter"):
			si_conditions.update({"transporter":filters.get("transporter")})
		if filters.get("sales_invoice"):
			si_conditions.update({"name":filters.get("sales_invoice")})
		sales_invoice=frappe.db.get_list("Sales Invoice", filters=si_conditions, fields=["rounded_total", "transporter", "name"])
		for si in sales_invoice:
			je_conditions=[["docstatus", "=", 1],["Journal Entry Account", "custom_sales_invoice", "=", si.name]]
			journal_entry=frappe.db.get_list("Journal Entry", filters=je_conditions, fields=["sum(`tabJournal Entry Account`.debit_in_account_currency) as debit_in_account_currency ", 
																					"sum(`tabJournal Entry Account`.credit_in_account_currency) as credit_in_account_currency", "name"])
			if journal_entry:
				si.invoice_no = si.name
				si.invoiced_value = si.rounded_total
				si.transporter = si.transporter
				si.auto_charge = journal_entry[0]['debit_in_account_currency'] or 0
		for si in sales_invoice:
			if si.auto_charge > 0:
				data.append(si)
	if not filters.get("voucher_type") or filters.get("voucher_type") == "Purchase Invoice":
		pi_conditions={"docstatus":1}
		if filters.get("from_date") and filters.get("to_date"):
			pi_conditions.update({"posting_date":["between", [filters.get("from_date"), filters.get("to_date")]]})
		if filters.get("custom_transporter"):
			pi_conditions.update({"transporter":filters.get("custom_transporter")})
		if filters.get("purchase_invoice"):
			pi_conditions.update({"name":filters.get("purchase_invoice")})
		purchase_invoice=frappe.db.get_list("Purchase Invoice", filters=pi_conditions, fields=["rounded_total", "custom_transporter", "name"])
		for pi in purchase_invoice:
			lcv_conditions=[["docstatus", "=", 1], ["Landed Cost Item", "receipt_document", "=", pi.name]]
			landed_cost=frappe.db.get_list("Landed Cost Voucher", filters=lcv_conditions, fields=["name"], group_by="name")
			for lc in landed_cost:
				lcv_amount_auto=frappe.db.get_list("Landed Cost Taxes and Charges", filters={"parent":lc.name, "custom_expense_type":"Auto Charge"}, fields=["sum(amount) as amount", "custom_expense_type"])
				lcv_amount_transport=frappe.db.get_list("Landed Cost Taxes and Charges", filters={"parent":lc.name, "custom_expense_type":"Transport Charge"}, fields=["sum(amount) as amount", "custom_expense_type"])
				pi.invoice_no = pi.name
				pi.invoiced_value =pi.rounded_total
				pi.transporter = pi.custom_transporter
				pi.auto_charge = lcv_amount_auto[0]["amount"] or 0
				pi.transport_charge = lcv_amount_transport[0]["amount"] or 0
		for pi in purchase_invoice:
			if pi.get("auto_charge") or pi.get("transport_charge"):
					data.append(pi)
			
	return data
