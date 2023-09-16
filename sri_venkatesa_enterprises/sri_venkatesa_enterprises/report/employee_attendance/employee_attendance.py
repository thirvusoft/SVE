# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import datetime


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data


def get_columns():
	is_admin_user = "SVE Admin" in frappe.get_roles()
	columns = [
		{
			"fieldname":"date",
			"label":"Date",
			"fieldtype":"Date",
			"width":150
		},
		{
			"fieldname":"employee",
			"label":"Employee",
			"fieldtype":"Link",
			"options":"Employee",
			"width":150
		},
		{
			"fieldname":"checkin_time",
			"label":"In Time",
			"fieldtype":"Time",
			"width":150
		},
		{
			"fieldname":"checkout_time",
			"label":"Out Time",
			"fieldtype":"Time",
			"width":150
		},
		{
			"fieldname":"total_hrs",
			"label":"Total Hrs",
			"fieldtype":"Time",
			"width":150,
			"hidden": not is_admin_user
		},
		{
			"fieldname":"start_km",
			"label":"Start Km",
			"fieldtype":"Float",
			"width":150,
			"hidden": not is_admin_user
		},
		{
			"fieldname":"end_km",
			"label":"End Km",
			"fieldtype":"Float",
			"width":150,
			"hidden": not is_admin_user
		},
		{
			"fieldname":"total_km",
			"label":"Total Km",
			"fieldtype":"Float",
			"width":150
		},
		{
			"fieldname":"actual_km",
			"label":"Actual Total Km",
			"fieldtype":"Float",
			"width":150,
			"hidden": not is_admin_user
		},
	]

	return columns

def get_data(filters={}):
	att_filter = {"employee":["is", "set"]}
	if filters.get("employee"):
		att_filter["employee"] = filters["employee"]
	if filters.get("from_date") and filters.get("to_date"):
		att_filter["attendance_date"] = ["between", (filters.get("from_date"), filters.get("to_date"))]
	elif filters.get("from_date"):
		att_filter["attendance_date"] = [">=", filters.get("from_date")]
	elif filters.get("to_date"):
		att_filter["attendance_date"] = ["<=", filters.get("to_date")]
	att_data = frappe.get_list("Employee In Out", filters=att_filter, fields=
		[
		"checkin_time as date",
		"employee", 
		"checkin_time",
		"checkout_time",
		"start_km",
		"end_km",
		"total_distance as total_km",
		"(end_km - start_km) as actual_km"
		])
	for i in att_data:
		if(i["checkout_time"] and i["checkin_time"]):
			i['total_hrs'] = (datetime.datetime.min + (i["checkout_time"] - i["checkin_time"])).time()
		if i["checkin_time"]:
			i["checkin_time"] = i["checkin_time"].strftime('%H:%M:%S')
		if i["checkout_time"]:
			i["checkout_time"] = i["checkout_time"].strftime('%H:%M:%S')
	return att_data