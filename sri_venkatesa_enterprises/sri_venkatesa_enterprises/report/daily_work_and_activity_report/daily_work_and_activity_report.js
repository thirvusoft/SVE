// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Daily Work and Activity Report"] = {
	"filters": [
		{
			fieldname:"employee",
			label:"Employee",
			fieldtype:"Link",
			options:"Employee"
		},
		{
			fieldname:"territory",
			label:"Territory",
			fieldtype:"Link",
			options:"Territory"
		},
		{
			fieldname:"from_date",
			label:"From Date",
			fieldtype:"Date",
			default:frappe.datetime.month_start() 
		},
		{
			fieldname:"to_date",
			label:"To Date",
			fieldtype:"Date",
			default:frappe.datetime.month_end()
		},
		{
			fieldname:"group_by_sales_person",
			label:"Group by Sales Person",
			fieldtype:"Check",
		},
	]
};
