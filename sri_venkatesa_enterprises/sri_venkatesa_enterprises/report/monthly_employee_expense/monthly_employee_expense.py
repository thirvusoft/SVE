# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe

from frappe.utils import add_days

def execute(filters=None):

	columns = get_columns(filters)

	data = get_data(filters)

	return columns, data

def get_columns(filters):

	columns = [

		{
			"fieldname": "employee_name",
			"label": "Employee Name",
			"fieldtype": "Data",
			"width": 170
		},

		{
			"fieldname": "actual_km_driven",
			"label": "Actual KM Driven",
			"fieldtype": "Int",
			"width": 170
		},

		{
			"fieldname": "km_updated_by_employee",
			"label": "KM Updated By Employee",
			"fieldtype": "Int",
			"width": 200
		},

		{
			"fieldname": "travel_expense",
			"label": "Travel Expense",
			"fieldtype": "Currency",
			"width": 170
		},

		{
			"fieldname": "daily_allowance",
			"label": "Daily Allowance",
			"fieldtype": "Currency",
			"width": 170
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

		employee_name_button = f'''<button style='background-color:#d3e9fc;'onclick='setroute(employee_name="{employee["name"]}", from_date="{filters.get("from_date")}", to_date="{filters.get("to_date")}")'>
		{employee["name"]}
		</button>
		'''

		sub_data = {
			"employee_name": employee_name_button,
			"actual_km_driven": 0,
			"km_updated_by_employee": 0,
			"travel_expense": 0,
			"daily_allowance": 0
		}

		checking_date = filters.get("from_date")

		while(checking_date <=  filters.get("to_date")):

			in_doc = frappe.get_all("Employee Checkin", {"employee": employee["name"], "log_type": "IN", "time": ["between", (checking_date, checking_date)]}, ["start_km"])

			out_doc = frappe.get_all("Employee Checkin", {"employee": employee["name"], "log_type": "OUT", "time": ["between", (checking_date, checking_date)]}, ["end_km", "vehicle_used", "total_km"])

			if in_doc and out_doc:

				sub_data["actual_km_driven"] += out_doc[0].end_km - in_doc[0].start_km

				sub_data["km_updated_by_employee"] += out_doc[0].total_km

				sub_data["travel_expense"] += frappe.get_all("Employee Vehicle Type", {"name": out_doc[0].vehicle_used},"allowance_per_km", pluck = "allowance_per_km")[0] * (out_doc[0].end_km - in_doc[0].start_km)

				sub_data["daily_allowance"] += employee["custom_daily_allowance"]

			checking_date = (add_days(checking_date, 1))

		data.append(sub_data)

	return data