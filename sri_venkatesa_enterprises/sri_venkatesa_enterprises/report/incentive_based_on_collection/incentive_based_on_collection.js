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
			"fieldname": "month",
			"label": __("Month"),
			"fieldtype": "Select",
			"reqd": 1 ,
			"options": [
				{ "value": 1, "label": __("Jan") },
				{ "value": 2, "label": __("Feb") },
				{ "value": 3, "label": __("Mar") },
				{ "value": 4, "label": __("Apr") },
				{ "value": 5, "label": __("May") },
				{ "value": 6, "label": __("June") },
				{ "value": 7, "label": __("July") },
				{ "value": 8, "label": __("Aug") },
				{ "value": 9, "label": __("Sep") },
				{ "value": 10, "label": __("Oct") },
				{ "value": 11, "label": __("Nov") },
				{ "value": 12, "label": __("Dec") },
			],
			"default": frappe.datetime.str_to_obj(frappe.datetime.get_today()).getMonth() + 1
		},
		{
			"fieldname":"year",
			"label": __("Year"),
			"fieldtype": "Select",
			"reqd": 1,
		},

	],
	onload: function() {
		return  frappe.call({
			method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.report.incentive_based_on_collection.incentive_based_on_collection.get_invoiced_years",
			callback: function(r) {
				var year_filter = frappe.query_report.get_filter('year');
				year_filter.df.options = r.message;
				year_filter.df.default = frappe.datetime.get_today().split("-")[0];
				year_filter.refresh();
				year_filter.set_input(year_filter.df.default);
			}
		});
	},
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if(data && (data.is_month_row==1 || data.is_row == 1) && data.eligible && ["Quarterly - Eligible", "Monthly - Eligible", "Half yearly - Eligible","Yearly - Eligible","Quarterly - Not Eligible", "Monthly - Not Eligible", "Half yearly - Not Eligible", "Yearly - Not Eligible"].includes(value)){
			if(data.eligible==1){
				value = "<b><span style='color:green;'>"+data.category+"</span></b>";
			}else{
				value = "<b><span style='color:red;'>"+data.category+"</span></b>";
			}
		}

		if(data && column.fieldname != "category" && data.is_month_row==1){
			value="<p style='text-align:left;'>"+value+"% </p>"
		}
		if(data && column.fieldname == "category" && value == "Total Eligible Amount"){
			value="<b><span style='color:darkgreen;'>"+data.category+"</span></b>"
		}

		if(data && column.fieldname == "incentive_percentage"){
			if(value){
				value="<p style='text-align:left;'>"+value+"% </p>"
				
			}
		}


		// if (data && data.indent == 0) {
		// 	data.credit = '';
		// 	data.debit = '';
		// 	data.cash='';
		// 	data.ff_online='';
		// 	value = "<b>" + value + "</b>";
		// 	if(column.fieldname != "voucher_type"){
		// 		value = "<p></p>"
		// 	}
		// }
		// if(data && column.fieldname == "mobile_no" && value == "Total"){
		// 	value = "<b>"+value+"</b>"
		// }
		// if(data && (data.mobile_no == "Total" || data.mobile_no == "<b>Total</b>") && (column.fieldname == "debit" || column.fieldname == "credit")){
		// 	value = "<b>" + value + "</b>"
		// }
		return value;
	},
};
