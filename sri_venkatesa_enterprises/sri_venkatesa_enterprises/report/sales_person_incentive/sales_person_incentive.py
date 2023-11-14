# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"fieldname":"item_group",
			"label":"Item Group",
			"fieldtype":"Link",
   			"options":"Item Group",
			"width":150
		},
		{
			"fieldname":"item_code",
			"label":"Item",
			"fieldtype":"Link",
			"options":"Item",
			"width":150
		},
		{
			"fieldname":"net_amount",
			"label":"Sales Achieved",
			"fieldtype":"Currency",
			"width":150
		},
		{
			"fieldname":"incentive_percentage",
			"label":"Incentive %",
			"fieldtype":"Float",
			"width":150
		},
		{
			"fieldname":"incentive_amount",
			"label":"Incentive amount",
			"fieldtype":"Currency",
			"width":150
		},
	]
	return columns
def get_data(filters):
	if filters.get("sales_type") == "Sales Invoice":
		conditions =[["posting_date", "between", [filters.get("from_date"), filters.get("to_date")]],
                ["docstatus", "=", 1],
                ["Sales Team", "sales_person", "=", filters.get("employee")],
                ]

		if filters.get("item_group"):
			conditions += [["Sales Invoice Item", "item_group", "=", filters.get("item_group")]]
		if filters.get("item"):
			conditions += [["Sales Invoice Item", "item_code", "=", filters.get("item")]]
		data_list=frappe.db.get_list("Sales Invoice", 
                            filters=conditions,
                            fields=["name","`tabSales Invoice Item`.item_code", "`tabSales Invoice Item`.item_group","sum(`tabSales Invoice Item`.net_amount) as net_amount" ,
                                    "`tabSales Invoice Item`.parent", "`tabSales Team`.sales_person"],
                            group_by="`tabSales Invoice Item`.item_code")
		for row in data_list:
			incentive_value=frappe.db.get_value("Employee Incentive Table", {"parent":row.item_group, "employee":row.sales_person, "item":row.item_code},"incentive_percentage")
			if not incentive_value:
				row.combine = True
				incentive_value=frappe.db.get_value("Employee Incentive Table", {"parent":row.item_group, "employee":row.sales_person, "item":["is", "not set"]},"incentive_percentage")
			row.incentive_amount=row.net_amount*(incentive_value/100)
			row.incentive_percentage=incentive_value
			row.sales_value=row.net_amount
			row.item=row.item_code
		item_group_incentive={}
		for group in data_list:
			key=(f"{group.item_group}, {group.incentive_percnetage}, {group.combine if group.combine else group.item_code}")
			if key not in item_group_incentive:
				item_group_incentive[key]=group
			else:
				item_group_incentive[key]["net_amount"]+=group.net_amount
				item_group_incentive[key]["incentive_amount"]+=group.incentive_amount
				item_group_incentive[key]["item_code"] =""
				
		return list(item_group_incentive.values())
	if filters.get("sales_type") == "Sales Order":
		conditions =[["transaction_date", "between", [filters.get("from_date"), filters.get("to_date")]],
                	["docstatus", "=", 1],
                	["Sales Team", "sales_person", "=", filters.get("employee")],
                	]
		if filters.get("item_group"):
			conditions += [["Sales Order Item", "item_group", "=", filters.get("item_group")]]
		if filters.get("item"):
			conditions += [["Sales Order Item", "item_code", "=", filters.get("item")]]
		data_list=frappe.db.get_list("Sales Order", 
                            filters=conditions, 
                            fields=["name","`tabSales Order Item`.item_code", "`tabSales Order Item`.item_group","sum(`tabSales Order Item`.net_amount) as net_amount" ,
                                    "`tabSales Order Item`.parent", "`tabSales Team`.sales_person"],
                            group_by="`tabSales Order Item`.item_code")
		for row in data_list:
			incentive_value=frappe.db.get_value("Employee Incentive Table", {"parent":row.item_group, "employee":row.sales_person, "item":row.item_code},"incentive_percentage")
			if not incentive_value:
				row.combine = True
				incentive_value=frappe.db.get_value("Employee Incentive Table", {"parent":row.item_group, "employee":row.sales_person, "item":["is", "not set"]},"incentive_percentage")
			row.incentive_amount=row.net_amount*(incentive_value/100)
			row.incentive_percentage=incentive_value
			row.sales_value=row.net_amount
			row.item=row.item_code
		item_group_incentive={}
		for group in data_list:
			key=(f"{group.item_group}, {group.incentive_percnetage}, {group.combine if group.combine else group.item_code}")
			if key not in item_group_incentive:
				item_group_incentive[key]=group
			else:
				item_group_incentive[key]["net_amount"]+=group.net_amount
				item_group_incentive[key]["incentive_amount"]+=group.incentive_amount
				item_group_incentive[key]["item_code"] =""
				
		return list(item_group_incentive.values())
	