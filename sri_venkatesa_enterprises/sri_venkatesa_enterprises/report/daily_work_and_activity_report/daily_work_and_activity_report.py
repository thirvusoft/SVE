# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_columns(filters={}):
	columns = [
		{
			"fildname":"date",
			"fieldtype":"Date",
			"label":"Date"
		},
		{
			"fildname":"party",
			"fieldtype":"Data",
			"label":"Customer/Farm"
		},
		{
			"fildname":"layers",
			"fieldtype":"Int",
			"label":"Layers"
		},
		{
			"fildname":"broilers",
			"fieldtype":"Int",
			"label":"Broilers"
		},
		{
			"fildname":"days",
			"fieldtype":"Int",
			"label":"No of Weeks/Days"
		},
		{
			"fildname":"date",
			"fieldtype":"Date",
			"label":"Date"
		},
		{
			"fildname":"item_code",
			"fieldtype":"Link",
			"label":"Demo of Product",
			"options":"Item"
		},
		{
			"fildname":"order_value",
			"fieldtype":"Currency",
			"label":"Order Value"
		},
		{
			"fildname":"collection_value",
			"fieldtype":"Currency",
			"label":"Collection Value"
		},
		{
			"fildname":"remarks",
			"fieldtype":"Data",
			"label":"Remarks"
		},		
	]

	return columns


def get_data(filters={}):
	data = []
	farm_details = []
	customer_wise_data = {}
	order_value_filters = {"docstatus":1}
	collection_value_filters = {"docstatus":1}
	if filters.get("date"):
		order_value_filters["posting_date"] = filters["date"]
		collection_value_filters["posting_date"] = filters["date"]
	if filters.get("territory"):
		lft, rgt = frappe.db.get_value("Territory", filters["territory"], ["lft", "rgt"])
		terr_list = frappe.get_list("Territory", filters={"lft":[">=", lft], "rgt":[">=", rgt]}, pluck="name")
		customer_list = frappe.get_list("Territory", filters={"territory":["in", terr_list]}, pluck="name")
		order_value_filters["customer"] = ["in", customer_list]
		collection_value_filters["party_type"] = "Customer"
		collection_value_filters["customer"] = ["in", customer_list]

	if collection_value_filters.get("customer"):
		farm_details = frappe.get_list("Farm Details", {"customer":["in", collection_value_filters["customer"]]}, fields=["sum(chick_capacity__laying) as laying", "customer as party"], group_by="customer")

	ordered_value = frappe.get_list("Sales Invoice", filters=order_value_filters, fields=["customer", "rounded_total"])
	collection_value = frappe.get_list("Payment Entry", filters=collection_value_filters, fields=["party", "paid_amount"])
	for i in ordered_value:
		customer_wise_data.setdefault(i["customer"], {}).setdefault("order_value", 0)
		customer_wise_data[i["customer"]]["order_value"] += i["rounded_total"]

	for i in collection_value:
		customer_wise_data.setdefault(i["party"], {}).setdefault("collection_value", 0)
		customer_wise_data[i["party"]]["collection_value"] += i["paid_amount"]

	opportunity_filter = {}
	if filters.get("date"):
		opportunity_filter["creation"] = filters["date"]
	if filters.get("territory"):
		lft, rgt = frappe.db.get_value("Territory", filters["territory"], ["lft", "rgt"])
		terr_list = frappe.get_list("Territory", filters={"lft":[">=", lft], "rgt":[">=", rgt]}, pluck="name")
		opportunity_filter["sub_route"] = ["in", terr_list]
	opportunity = frappe.get_list("Opportunity", filters=opportunity_filter, pluck="name")
	opportunity_data = frappe.get_all("Opportunity Item", filters={"parent":["in", opportunity]}, fields=["parent as party", "item_code"])
	for i in opportunity_data:
		opp_from, party = frappe.db.get_value("Opportunity", i["party"], ["opportunity_from", "party_name"])
		if opp_from == "Customer":
			i["party"] = party
		elif opp_from == "Lead":
			farm_details.extend(frappe.get_list("Farm Details", {"lead": i["party"]}, fields=["sum(chick_capacity__laying) as laying", "lead as party"], group_by="lead"))
			customer = frappe.db.get_value("Customer", {"from_lead":i["party"]}, "name")
			if customer:
				i["party"] = "Customer"
		customer_wise_data.setdefault(i["party"], {}).setdefault("item_code", "")
		if not customer_wise_data[i["party"]]["item_code"]:
			customer_wise_data[i["party"]]["item_code"] = i["item_code"]
		else:
			customer_wise_data[i["party"]]["item_code"] += f""", {i["item_code"]}"""
	
	for i in farm_details:
		if i["party"] in customer_wise_data:
			customer_wise_data[i["party"]]["layers"] = i["laying"]

	return list(customer_wise_data.values())
	