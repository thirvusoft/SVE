# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns, data = get_columns(filters), get_data(filters)
	return columns, data


def get_columns(filters={}):
	columns = [
		{
			"fieldname":"date",
			"fieldtype":"Date",
			"label":"Date",
			"default": filters.get("date") or ""
		},
		{
			"fieldname":"party",
			"fieldtype":"Data",
			"label":"Customer/Farm"
		},
		{
			"fieldname":"layers",
			"fieldtype":"Int",
			"label":"Layers"
		},
		{
			"fieldname":"broilers",
			"fieldtype":"Int",
			"label":"Broilers"
		},
		{
			"fieldname":"days",
			"fieldtype":"Int",
			"label":"No of Weeks/Days"
		},
		{
			"fieldname":"item_code",
			"fieldtype":"Link",
			"label":"Demo of Product",
			"options":"Item"
		},
		{
			"fieldname":"order_value",
			"fieldtype":"Currency",
			"label":"Order Value"
		},
		{
			"fieldname":"collection_value",
			"fieldtype":"Currency",
			"label":"Collection Value"
		},
		{
			"fieldname":"remarks",
			"fieldtype":"Data",
			"label":"Remarks",
			"width":300
		},		
	]

	return columns

def get_data(filters={}):
	if not filters.get("group_by_sales_person"):
		return get_report_data(filters)
	else:
		final_data = []
		employee_list = frappe.get_list("Employee", filters={"status":["!=", "Inactive"]}, fields=["name", "employee_name"])
		for i in employee_list:
			filters["employee"] = i["name"]
			user = frappe.db.get_value("Employee", filters["employee"], "user_id")
			if user:
				territory = frappe.db.get_value("User Permission", {"user":user, "allow":"Territory"}, "for_value")
				if territory:
					filters["territory"] = territory
			final_data.append({"party":f"<b>Emp: {i['employee_name']}</b>"})
			final_data.extend(get_report_data(filters))
			final_data.append({})
		return final_data

def get_report_data(filters={}):
	data = []
	user = None
	if filters.get("employee"):
		user = frappe.db.get_value("Employee", filters["employee"], "user_id")
		if user:
			territory = frappe.db.get_value("User Permission", {"user":user, "allow":"Territory"}, "for_value")
			if territory:
				filters["territory"] = territory
		if not user:
			frappe.msgprint(f"""Employee doesn't link with any user. <a href='/app/employee/{filters["employee"]}'>Click to Link</a>""")
			return []
	farm_details = []
	customer_wise_data = {}
	order_value_filters = {"docstatus":1}
	collection_value_filters = {"docstatus":1}

	if user:
		collection_value_filters["owner"] = user

	if filters.get("date"):
		order_value_filters["posting_date"] = filters["date"]
		collection_value_filters["posting_date"] = filters["date"]
	if filters.get("territory"):
		lft, rgt = frappe.db.get_value("Territory", filters["territory"], ["lft", "rgt"])
		terr_list = frappe.get_list("Territory", filters={"lft":[">=", lft], "rgt":["<=", rgt]}, pluck="name")
		customer_list = frappe.get_list("Customer", filters={"territory":["in", terr_list]}, pluck="name")
		order_value_filters["customer"] = ["in", customer_list]
		collection_value_filters["party_type"] = "Customer"
		collection_value_filters["party"] = ["in", customer_list]

	farm_filter = {}
	if collection_value_filters.get("customer"):
		# farm_filter = {"customer":["in", collection_value_filters["party"]]}
	
		farm_details = frappe.get_list("Farm Details", filters={"customer":["in", collection_value_filters["party"]]}, fields=["sum(chick_capacity__laying) as laying", "customer as party"], group_by="customer")

	ordered_value = frappe.get_list("Sales Invoice", filters=order_value_filters, fields=["customer", "rounded_total"])
	collection_value = frappe.get_list("Payment Entry", filters=collection_value_filters, fields=["party", "paid_amount"])
	for i in ordered_value:
		customer_wise_data.setdefault(i["customer"], {"party":i["customer"]}).setdefault("order_value", 0)
		customer_wise_data[i["customer"]]["order_value"] += i["rounded_total"]

	for i in collection_value:
		customer_wise_data.setdefault(i["party"], {"party":i["party"]}).setdefault("collection_value", 0)
		customer_wise_data[i["party"]]["collection_value"] += i["paid_amount"]

	opportunity_filter = {}
	if user:
		opportunity_filter["owner"] = user
	if filters.get("date"):
		opportunity_filter["creation"] = ["between", (f"""{filters["date"]} 00:00:00""", f"""{filters["date"]} 23:59:59""")]
	if filters.get("territory"):
		lft, rgt = frappe.db.get_value("Territory", filters["territory"], ["lft", "rgt"])
		terr_list = frappe.get_list("Territory", filters={"lft":[">=", lft], "rgt":["<=", rgt]}, pluck="name")
		opportunity_filter["territory"] = ["in", terr_list]
	opportunity = frappe.get_list("Opportunity", filters=opportunity_filter, fields=["name as party", "opportunity_from", "party_name", "name as opportunity", "remarks"])


	opportunity_party_map = {}
	opportunity_remark_map = {}
	for i in opportunity:
		# opp_from, party = frappe.db.get_value("Opportunity", i["party"], ["opportunity_from", "party_name"])
		if i["opportunity_from"] == "Customer":
			i["party"] = i["party_name"]
		elif i["opportunity_from"] == "Lead":
			customer = frappe.db.get_value("Customer", {"lead_name":i["party_name"]}, "name")
			if customer:
				i["party"] = customer
				
		customer_farm = frappe.get_list("Farm Details", filters={"customer": i["party"]}, fields=["sum(chick_capacity__laying) as laying", "customer as party", "name"], group_by="customer")
		lead_form = frappe.get_list("Farm Details", filters={"lead": i["party_name"], "name":["not in", [j["name"] for j in customer_farm]]}, fields=["sum(chick_capacity__laying) as laying", "lead as party"], group_by="lead")
		farm_details.extend(customer_farm+lead_form)

		# doc=frappe.get_doc("Opportunity", i["opportunity"])
		opportunity_remark_map[i["opportunity"]] = i.get("remarks") or ""
		# if doc.follow_up:
			# opportunity_remark_map[i["opportunity"]] = doc.follow_up[-1].description
		opportunity_party_map[i["opportunity"]] = i["party"]

	opportunity_data = frappe.get_all("Opportunity Item", filters={"parent":["in", [j["opportunity"] for j in opportunity]]}, fields=["parent as party", "item_code"])

	for i in opportunity_remark_map:
		remarks = opportunity_remark_map[i]
		customer_wise_data.setdefault(opportunity_party_map[i], {"party":opportunity_party_map[i]}).setdefault("remarks", 0)
		customer_wise_data[opportunity_party_map[i]]["remarks"] = remarks
	for i in opportunity_data:
		remarks = opportunity_remark_map.get(i["party"]) or ""
		i["party"] = opportunity_party_map.get(i["party"]) or i["party"]
		customer_wise_data.setdefault(i["party"], {"party":i["party"]}).setdefault("item_code", "")
		if not customer_wise_data[i["party"]]["item_code"]:
			customer_wise_data[i["party"]]["item_code"] = i["item_code"]
		else:
			customer_wise_data[i["party"]]["item_code"] += f""", {i["item_code"]}"""
		
	for i in farm_details:
		if i["party"] in customer_wise_data:
			customer_wise_data[i["party"]]["layers"] = i["laying"]
		else:
			customer_wise_data[i["party"]] = {"layers":i["laying"], "party":i["party"]}

	return list(customer_wise_data.values())
	