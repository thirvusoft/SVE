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
			fieldname:"date",
			label:"Date",
			fieldtype:"Date",
		},
	]
};
