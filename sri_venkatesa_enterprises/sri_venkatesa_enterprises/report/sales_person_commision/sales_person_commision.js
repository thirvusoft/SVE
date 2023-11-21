// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Commision"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label":"Employee",
			"fieldtype":"Link",
			"options":"Sales Person",
			"reqd":1
		},
		{
			"fieldname":"from_date",
			"label":"From Date",
			"fieldtype":"Date",
			"default":frappe.datetime.month_start(),
			"reqd":1
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype":"Date",
			"default":frappe.datetime.month_end() ,
			"reqd":1
		},
		{
			"fieldname":"item_group",
			"label":"Item Group",
			"fieldtype":"Link",
			"options":"Item Group"
		},
		{
			"fieldname":"item",
			"label":"Item",
			"fieldtype":"Link",
			"options":"Item"
		},
		{
			"fieldname":"sales_type",
			"label":"Sales Type",
			"fieldtype":"Select",
			"options":["Sales Order","Sales Invoice"],
			"default":"Sales Invoice"
		},
		
	]
};
