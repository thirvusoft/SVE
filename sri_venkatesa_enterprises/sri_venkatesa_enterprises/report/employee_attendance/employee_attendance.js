// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Employee Attendance"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label":"Employee",
			"fieldtype":"Link",
			"options":"Employee"
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
		}
	]
};
