// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Incentive Based on Collection"] = {
	"filters": [
		{
			"fieldname":"sales_person",
			"label":"Sales Person",
			"fieldtype":"Link",
			"options":"Sales Person",
			"reqd":1
		},
		{
			"fieldname":"from_date",
			"label":"From Date",
			"fieldtype":"Date",
			"reqd":1
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype":"Date",
			"reqd":1
		},

	]
};
