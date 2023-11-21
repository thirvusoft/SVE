# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import datetime
from frappe.utils import get_time


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

def get_data(filters={}):
	att_filter = {"employee":["is", "set"]}
	if filters.get("employee"):
		att_filter["employee"] = filters["employee"]
	if filters.get("from_date") and filters.get("to_date"):
		att_filter["time"] = ["between", (filters.get("from_date"), filters.get("to_date"))]
	elif filters.get("from_date"):
		att_filter["time"] = [">=", filters.get("from_date")]
	elif filters.get("to_date"):
		att_filter["time"] = ["<=", filters.get("to_date")]
	# Extract the date part from the 'time' field
	att_data = frappe.get_list("Employee Checkin", filters=att_filter, fields=[
		"DATE(time) as date",
		"employee"
	], group_by= 'employee,date')
	
	for i in att_data:
		if frappe.get_all('Employee Checkin',{'log_type':'IN','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time'):
			i['checkin_time'] = get_time(frappe.get_all('Employee Checkin',{'log_type':'IN','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time')[0]['time'])
		
		if frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time'):
			i['checkout_time'] = get_time(frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time')[0]['time'])
			
		if(i.get("checkout_time") and i.get("checkin_time")):
			i['total_hrs'] = (datetime.datetime.min + (frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time')[0]['time']- frappe.get_all('Employee Checkin',{'log_type':'IN','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'time')[0]['time'])).time()

		if frappe.get_all('Employee Checkin',{'log_type':'IN','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'start_km'):
			i['start_km'] = frappe.get_all('Employee Checkin',{'log_type':'IN','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'start_km')[0]['start_km']
			
		if frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'end_km'):
			i['end_km'] = frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'end_km')[0]['end_km']
		
		if frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'total_km'):
			i['total_km'] = frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'total_km')[0]['total_km']

		if i.get('start_km') and i.get('end_km'):
			i['actual_km'] = i.get('end_km') - i.get('start_km')

			vehicle_used = frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':i.get('employee'),'time':('between',[i.get('date'),i.get('date')])},'vehicle_used')[0]['vehicle_used']

			i["travel_expense"] = frappe.get_all("Employee Vehicle Type", {"name": vehicle_used},"allowance_per_km", pluck = "allowance_per_km")[0] * i['actual_km']

			i["daily_allowance"] = frappe.get_value("Employee", {"name": i.get('employee')}, "custom_daily_allowance")
			
	return att_data