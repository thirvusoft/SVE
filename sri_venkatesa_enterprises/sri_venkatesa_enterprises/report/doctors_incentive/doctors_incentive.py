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
			"fieldname":"stock_qtys",
			"label":"Stock Qty",
			"fieldtype":"Float",
			"width":150
		},
		{
			"fieldname":"incentive_amount_per_stockqty",
			"label":"Incentive Amount Per Stock Qty",
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
		sales_invoice=frappe.db.get_list("Sales Invoice", filters=[
      			["posting_date", "between", [filters.get("from_date"), filters.get("to_date")]],
                ["docstatus", "=", 1],
                ["Sales Team", "sales_person", "=",filters.get("doctor")]
                ], pluck="name")  
		conditions={"parent":["in", sales_invoice]}
		if filters.get("item_group"):
			conditions.update({"item_group":filters.get("item_group")})
		if filters.get("item"):
			conditions.update({"item_code":filters.get("item")})
		data_list=frappe.db.get_list("Sales Invoice Item", 
                            filters=conditions,
                            fields=["item_code", "item_group","sum(net_amount) as net_amount" ,
                                    "sum(stock_qty) as stock_qty" , "parent"],
							group_by="item_code"
                            )
		for row in data_list:
			incentive_value=frappe.db.get_value("Doctor Incentive Table", {"parent":row.item_group, "doctor":filters.get("doctor"), "item":row.item_code},"incentive_amount")
			if not incentive_value:
				row.combine = True
				incentive_value=frappe.db.get_value("Doctor Incentive Table", {"parent":row.item_group, "doctor":filters.get("doctor"), "item":["is", "not set"]},"incentive_amount") or 0
			
			row.sales_value=row.net_amount
			row.stock_qtys=row.stock_qty
			row.incentive_amount=(row.stock_qty or 0)*(incentive_value or 0)
			row.incentive_amount_per_stockqty=incentive_value
			row.item=row.item_code

   
		item_group_incentive={}
		for group in data_list:
			key=(f"{group.item_group}, {group.incentive_amount_per_stockqty}, {group.combine if group.combine else group.item_code}")
			if key not in item_group_incentive:
				item_group_incentive[key]=group
			else:
				item_group_incentive[key]["net_amount"]+=group.net_amount
				item_group_incentive[key]["incentive_amount"]+=group.incentive_amount
				item_group_incentive[key]["stock_qtys"]+=group.stock_qtys
				item_group_incentive[key]["item_code"] =""
				
		return list(item_group_incentive.values())
	if filters.get("sales_type") == "Sales Order":
		sales_order =frappe.db.get_list("Sales Order", filters=[
      				["transaction_date", "between", [filters.get("from_date"), filters.get("to_date")]],
                	["docstatus", "=", 1],
                	["Sales Team", "sales_person", "=", filters.get("doctor")],
                	], pluck="name")
		conditions={"parent":["in", sales_order]}
		if filters.get("item_group"):
			conditions.update({"item_group": filters.get("item_group")})
		if filters.get("item"):
			conditions.update({"item_code":filters.get("item")})
		data_list=frappe.db.get_list("Sales Order Item", 
                            filters=conditions, 
                            fields=["item_code", "item_group","sum(net_amount) as net_amount" ,
                                    "sum(stock_qty) as stock_qty", "parent"],
                            group_by="item_code")
		for row in data_list:
			incentive_value=frappe.db.get_value("Doctor Incentive Table", {"parent":row.item_group, "doctor":filters.get("doctor"), "item":row.item_code},"incentive_amount")
			if not incentive_value:
				row.combine = True
				incentive_value=frappe.db.get_value("Doctor Incentive Table", {"parent":row.item_group, "doctor":filters.get("doctor"), "item":["is", "not set"]},"incentive_amount")
			row.incentive_amount=(row.stock_qty or 0) * (incentive_value or 0)
			row.incentive_amount_per_stockqty=incentive_value
			row.stock_qtys = row.stock_qty
			row.sales_value=row.net_amount
			row.item=row.item_code
		item_group_incentive={}
		for group in data_list:
			key=(f"{group.item_group}, {group.incentive_amount_per_stockqty}, {group.combine if group.combine else group.item_code}")
			if key not in item_group_incentive:
				item_group_incentive[key]=group
			else:
				item_group_incentive[key]["net_amount"]+=group.net_amount
				item_group_incentive[key]["incentive_amount"]+=group.incentive_amount
				item_group_incentive[key]["stock_qtys"]+=group.stock_qtys
				item_group_incentive[key]["item_code"] =""
				
		return list(item_group_incentive.values())
	