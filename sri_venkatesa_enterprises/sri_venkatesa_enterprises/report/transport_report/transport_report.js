// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Transport Report"] = {
	"filters": [
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
			"fieldname":"voucher_type",
			"label":"Voucher Type",
			"fieldtype":"Select",
			"options":[" ", "Sales Invoice", "Purchase Invoice"],
			on_change: function() {
				let voucher_type = frappe.query_report.get_filter_value('voucher_type');
				frappe.query_report.toggle_filter_display('sales_invoice', (voucher_type === 'Purchase Invoice' ));
				frappe.query_report.toggle_filter_display('purchase_invoice',( voucher_type === 'Sales Invoice'  ));
				frappe.query_report.refresh();
			}
		},
		{
			"fieldname":"sales_invoice",
			"label":"Invoice No",
			"fieldtype":"Link",
			"options":"Sales Invoice",
			"hidden":1

		},
		{
			"fieldname":"purchase_invoice",
			"label":"Invoice No",
			"fieldtype":"Link",
			"options":"Purchase Invoice",
			"hidden":1
		},
		{
			"fieldname":"transporter",
			"label":"Transporter",
			"fieldtype":"Link",
			"options":"Supplier",
			"get_query": function () {
				var unit = frappe.query_report.get_filter_value('transporter');
				return {
					filters: [
						["Supplier", "is_transporter", "=", 1],
					]
				};
			},
		},
		
	],
};

