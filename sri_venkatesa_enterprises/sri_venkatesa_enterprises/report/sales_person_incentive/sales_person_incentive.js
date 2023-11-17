// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Person Incentive"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label":"Employee",
			"fieldtype":"Link",
			"options":"Sales Person"
		},
		{
			"fieldname":"from_date",
			"label":"From Date",
			"fieldtype":"Date",
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype":"Date",
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
