// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt
frappe.provide('sve');
var login_btn, logout_btn;

frappe.ui.form.on('Daily Activity', {
	refresh: function (frm) {
		if (frm.is_new()) {
			frm.call({
				doc: frm.doc,
				method: "get_employee_id",
				callback(r) {
					frm.refresh_field("employee")
				}
			});
			frm.trigger('date');
		}
		var field_map = {
			"for_customer":{"field":"customer_type", "value":"Customer"},
			"for_doctor_and_dealer":{"field":"customer_type", "value":["in", ["Doctor", "Dealer"]]},
			"appointments":{"field":"customer_type", "value":["in", ["Doctor", "Dealer", "Customer"]]}
		};
		['for_customer', 'for_doctor_and_dealer', 'appointments'].forEach(table => {
			
			frm.set_query('customer', table, function () {
				var field = field_map[table]["field"];
				var qry_filters = {
					do_not_contact: 0,
				}
				qry_filters[field] = field_map[table]["value"]
				return {
					filters: qry_filters
				}
			});
		});

		(frm.doc.for_doctor_and_dealer || []).concat(frm.doc.for_customer || []).concat(frm.doc.appointments || []).forEach(row => {
			frm.fields_dict[row.parentfield].grid.grid_rows[row.idx - 1].make_control(frm.fields_dict[row.parentfield].grid.grid_rows[row.idx - 1].columns.create)
		});

		frm.trigger("add_login_and_logout_btn");
	},
	login_logout_btn_visibility: function (frm) {
		if (login_btn && logout_btn) {

			document.querySelector(`button[data-fieldtype="Button"][data-fieldname="login"]`).classList.add('btn-primary')
			document.querySelector(`button[data-fieldtype="Button"][data-fieldname="logout"]`).classList.add('btn-primary')


			function btnVisible() {
				window.requestAnimationFrame(btnVisible);
				if (sve.isVisible(login_btn[0])) {
					frm.set_df_property('login', 'hidden', 1)
				} else {
					frm.set_df_property('login', 'hidden', 0)
				}

				if (sve.isVisible(logout_btn[0])) {
					frm.set_df_property('logout', 'hidden', 1)
				} else {
					frm.set_df_property('logout', 'hidden', 0)
				}
			}

			try {
				btnVisible();;
			} catch (error) {
				console.log('Error caught:', error);
			}
		}
	},
	login: function (frm) {
		let dialog = new frappe.ui.Dialog({
			title:"Enter Start Km",
			fields:[
				{fieldname:"start_km", label:"Start Km", fieldtype:"Float", reqd:1},
				{fieldtype:"Column Break"},
				{fieldname:"vehicle_used", label:"Vehicle Used", fieldtype:"Link", reqd:1, options:"Employee Vehicle Type", default:"BIKE"}
			],
			primary_action(data){
				if(!data.start_km){
					frappe.throw("Start Km is Mandatory")
				}
				else{
					frappe.call({
						method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee_checkin.create_checkin",
						args:{
							start_km:data.start_km,
							vehicle_used:data.vehicle_used
						},
						callback(r){
							if(r.message == 'Checkin already created'){
								frappe.show_alert({"message":"Checkin Already Created", "indicator":"yellow"})
							}
							else if(r.message){
								frappe.show_alert({"message":"Checkin Created Successfully", "indicator":"green"})
							}
							else{
								frappe.show_alert({"message":"<p>Failed to Create Checkin</p><p>Click on <b>Add Employee Checkin</b> to create checkin</p>", "indicator":"red"})
							}
							dialog.hide()
						}
					})
				}
			}
		})
		dialog.show()
	},
	logout: function (frm) {
		let dialog = new frappe.ui.Dialog({
			title:"Enter End Km",
			fields:[
				{fieldname:"end_km", label:"End Km", fieldtype:"Float", reqd:1},
				{fieldname:"total_km", label:"Total Km", fieldtype:"Float", reqd:1}
			],
			primary_action(data){
				if(!data.end_km){
					frappe.throw("End Km is Mandatory")
				}
				else if(!data.total_km){
					frappe.throw("Total Km is Mandatory")
				}
				else{
					frappe.call({
						method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee_checkin.create_checkout",
						args:{
							end_km:data.end_km,
							total_km:data.total_km
						},
						callback(r){
							if(r.message == 'Checkout Already Created'){
								frappe.show_alert({"message":"Checkout Already Created", "indicator":"yellow"})
							}
							else if(r.message){
								frappe.show_alert({"message":"CheckOut Created Successfully", "indicator":"green"})
							}
							else{
								frappe.show_alert({"message":"<p>Failed to Create CheckOut</p>", "indicator":"red"})
							}
							dialog.hide()
						}
					})
				}
			}
		})
		frappe.call({
			method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee_checkin.validate_checkout",
			callback(r){
				if(r.message){
					dialog.show()
				}
			}
		})
	},
	add_login_and_logout_btn: function (frm) {
		login_btn = frm.add_custom_button(__("Login"), function () {
			frm.trigger('login')
		}).addClass('btn-primary')

		logout_btn = frm.add_custom_button(__("Logout"), function () {
			frm.trigger('logout')
		}).addClass('btn-primary')
		frm.trigger('login_logout_btn_visibility');
	},
	date: function (frm) {
		if (frm.doc.date) {
			(frm.doc.for_doctor_and_dealer || []).concat(frm.doc.for_customer || []).concat(frm.doc.appointments || []).forEach(row => {
				let cdt = row.doctype, cdn = row.name;
				if (row.customer) {
					frappe.call({
						method: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.get_customer_order_ids_and_values',
						args: {
							customer: row.customer,
							date: frm.doc.date
						},
						callback: function (r) {
							if (row.parentfield == 'appointments') {
								frappe.model.set_value(cdt, cdn, 'outstanding_amount', r.message.outstanding_amount || '');
								frappe.model.set_value(cdt, cdn, 'collection_value', r.message.paid_amount || '');
							} else {
								frappe.model.set_value(cdt, cdn, 'order_id', r.message.ids || '');
								frappe.model.set_value(cdt, cdn, 'order_value', r.message.values || '');
								frappe.model.set_value(cdt, cdn, 'outstanding', r.message.outstanding_amount || '');
								frappe.model.set_value(cdt, cdn, 'collection_value', r.message.paid_amount || '');
							}
						}
					});
				}
			});
		}
	}
});

frappe.ui.form.on("Customer Daily Activity", {
	customer: async function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		if (data.customer) {
			let res = await frappe.db.get_list('Farm Details', { filters: { 'customer': data.customer }, fields: ['sum(chick_capacity__laying) as ccl'] });
			frappe.model.set_value(cdt, cdn, 'batch_size', (res && res[0] && res[0].ccl) ? res[0].ccl : 0);
			if (frm.doc.date) {
				frappe.call({
					method: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.get_customer_order_ids_and_values',
					args: {
						customer: data.customer,
						date: frm.doc.date
					},
					callback: function (r) {
						frappe.model.set_value(cdt, cdn, 'order_id', r.message.ids || '');
						frappe.model.set_value(cdt, cdn, 'order_value', r.message.values || '');
						frappe.model.set_value(cdt, cdn, 'outstanding', r.message.outstanding_amount || '');
						frappe.model.set_value(cdt, cdn, 'collection_value', r.message.paid_amount || '');
					}
				});
			}
		}
	},
	for_customer_add: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		frm.fields_dict.for_customer.grid.grid_rows[data.idx - 1].make_control(frm.fields_dict.for_customer.grid.grid_rows[data.idx - 1].columns.create)
	},
	create: function (frm, cdt, cdn) {
		show_create_dialog(frm, cdt, cdn)
	}
});

frappe.ui.form.on("Doctor Dealer Daily Activity", {
	customer: async function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		if (data.customer) {
			if (frm.doc.date) {
				frappe.call({
					method: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.get_customer_order_ids_and_values',
					args: {
						customer: data.customer,
						date: frm.doc.date
					},
					callback: function (r) {
						frappe.model.set_value(cdt, cdn, 'order_id', r.message.ids || '');
						frappe.model.set_value(cdt, cdn, 'order_value', r.message.values || '');
						frappe.model.set_value(cdt, cdn, 'outstanding', r.message.outstanding_amount || '');
						frappe.model.set_value(cdt, cdn, 'collection_value', r.message.paid_amount || '');
					}
				});
			}
		}
	},
	for_doctor_and_dealer_add: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		frm.fields_dict.for_doctor_and_dealer.grid.grid_rows[data.idx - 1].make_control(frm.fields_dict.for_doctor_and_dealer.grid.grid_rows[data.idx - 1].columns.create)
	},
	create: function (frm, cdt, cdn) {
		show_create_dialog(frm, cdt, cdn)
	}
});

frappe.ui.form.on("Daily Activity Appointments", {
	customer: async function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		if (data.customer) {
			if (frm.doc.date) {
				frappe.call({
					method: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.get_customer_order_ids_and_values',
					args: {
						customer: data.customer,
						date: frm.doc.date
					},
					callback: function (r) {
						frappe.model.set_value(cdt, cdn, 'outstanding_amount', r.message.outstanding_amount || '');
						frappe.model.set_value(cdt, cdn, 'collection_value', r.message.paid_amount || '');
					}
				});
			}
		}
	},
	appointments_add: function (frm, cdt, cdn) {
		let data = locals[cdt][cdn];
		frm.fields_dict.appointments.grid.grid_rows[data.idx - 1].make_control(frm.fields_dict.appointments.grid.grid_rows[data.idx - 1].columns.create)
	},
	create: function (frm, cdt, cdn) {
		show_create_dialog(frm, cdt, cdn)
	}
});

function show_create_dialog(frm, cdt, cdn) {
	let d = new frappe.ui.Dialog({
		title: 'Create',
		fields: [
			{
				fieldname: "sales_order",
				label: __("Sales Order"),
				fieldtype: "Button",
				click: function () {
					let row = locals[cdt][cdn]
					frappe.new_doc('Sales Order', { 'customer': row.customer });
				}
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldname: "payment_entry",
				label: __("Payment Entry"),
				fieldtype: "Button",
				click: function () {
					let row = locals[cdt][cdn]
					frappe.new_doc('Payment Entry', {
						'payment_type': 'Receive',
						'party_type': 'Customer',
						'party': row.customer,
					}).then(() => {
						cur_frm.set_value('party', row.customer);
					});
				}
			},
		]
	});

	d.show();
}
