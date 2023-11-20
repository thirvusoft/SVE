# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

def execute(filters=None):

	columns = get_columns(filters)

	data = get_data(filters)

	return columns, data

def get_columns(filters):

	columns = [

		{
			"fieldname": "employee_id",
			"label": "Employee ID",
			"fieldtype": "Link",
   			"options": "Employee",
			"width": 150
		},

		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 150
		},

		{
			"fieldname": "actual_km_driven",
			"label": "Actual KM Driven",
			"fieldtype": "Int",
			"width": 150
		},

		{
			"fieldname": "km_updated_by_employee",
			"label": "KM Updated By Employee",
			"fieldtype": "Int",
			"width": 150
		},

		{
			"fieldname": "travel_expense",
			"label": "Travel Expense",
			"fieldtype": "Currency",
			"width": 150
		},

		{
			"fieldname": "daily_allowance",
			"label": "Daily Allowance",
			"fieldtype": "Currency",
			"width": 150
		}

	]

	return columns

def get_data(filters):

	data = []

	if filters.get("employee"):

		employee_list = frappe.get_all("Employee", {"status": "Active", "name": filters.get("employee")}, ["name", "custom_daily_allowance"])

	else:

		employee_list = frappe.get_all("Employee", {"status": "Active"}, ["name", "custom_daily_allowance"])

	for employee in employee_list:

		

	return data