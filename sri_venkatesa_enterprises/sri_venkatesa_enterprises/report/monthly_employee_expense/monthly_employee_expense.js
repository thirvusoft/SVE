// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Monthly Employee Expense"] = {
	"filters": [
		{
			"fieldname":"employee",
			"label":"Employee",
			"fieldtype":"Link",
			"options":"Employee",
			"get_query": function() {
				return {
					filters: {
						"status": "Active"
					}
				};
			}
		},
		{
			"fieldname":"from_date",
			"label":"From Date",
			"fieldtype":"Date",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.month_start(), -0)
		},
		{
			"fieldname":"to_date",
			"label":"To Date",
			"fieldtype":"Date",
			"reqd": 1,
			"default": frappe.datetime.now_date()
		}
	]
};

function setroute(employee_name, from_date, to_date){
	console.log(from_date)
	frappe.route_options = {

		employee: employee_name,
		from_date: from_date,
		to_date: to_date
	   };
	   frappe.set_route("query-report", "Employee Attendance")
}