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
			"fieldname":"month",
			"label":"Month",
			"fieldtype":"Select",
			"reqd":1,
			"options": [
                { "value": 1, "label": __("January") },                
				{ "value": 2, "label": __("February") },
                { "value": 3, "label": __("March") },                
				{ "value": 4, "label": __("April") },
                { "value": 5, "label": __("May") },                
				{ "value": 6, "label": __("June") },
                { "value": 7, "label": __("July") },                
				{ "value": 8, "label": __("August") },
                { "value": 9, "label": __("September") },                
				{ "value": 10, "label": __("October") },
                { "value": 11, "label": __("November") },                
				{ "value": 12, "label": __("December") },
            ],
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1,
		},
		{
			"fieldname":"year",
			"label":"Year",
			"fieldtype":"Select",
			"options": [],
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
		
	],
	onload: () => {
		let today=frappe.datetime.get_today()
		let year = parseInt(today.split("-")[0])
		let years=[year-2, year-1, year, year+1, year+2]
		frappe.query_report.get_filter("year").df.options=years
		frappe.query_report.get_filter("year").set_options(year) 
		frappe.query_report.set_filter_value("year", year)

	}
};
