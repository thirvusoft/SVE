// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

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
		}

		['for_customer', 'for_doctor_and_dealer', 'appointments'].forEach(table => {
			frm.set_query('customer', table, function () {
				return {
					filters: {
						do_not_contact: 0
					}
				}
			});
		});

		(frm.doc.for_doctor_and_dealer || []).concat(frm.doc.for_customer || []).forEach(row => {
			frm.fields_dict[row.parentfield].grid.grid_rows[row.idx - 1].make_control(frm.fields_dict[row.parentfield].grid.grid_rows[row.idx - 1].columns.create)
		});

		frm.trigger("add_login_and_logout_btn");
	},
	add_login_and_logout_btn: function (frm) {
		frm.add_custom_button(__("Login"), function () {
			let dialog = new frappe.ui.Dialog({
				title: "Enter Start Km",
				fields: [
					{ fieldname: "start_km", label: "Start Km", fieldtype: "Float", reqd: 1 }
				],
				primary_action(data) {
					if (!data.start_km) {
						frappe.throw("Start Km is Mandatory")
					}
					else {
						frappe.call({
							method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.create_checkin",
							args: {
								start_km: data.start_km
							},
							callback(r) {
								if (r.message) {
									frappe.show_alert({ "message": "Checkin Created Successfully", "indicator": "green" })
								}
								else {
									frappe.show_alert({ "message": "<p>Failed to Create Checkin</p><p>Click on <b>Add Employee In Out</b> to create checkin</p>", "indicator": "red" })
								}
								dialog.hide()
							}
						})
					}
				}
			})
			dialog.show()

		})

		frm.add_custom_button(__("Logout"), function () {
			let dialog = new frappe.ui.Dialog({
				title: "Enter End Km",
				fields: [
					{ fieldname: "end_km", label: "End Km", fieldtype: "Float", reqd: 1 },
					{ fieldname: "total_km", label: "Total Km", fieldtype: "Float", reqd: 1 }
				],
				primary_action(data) {
					if (!data.end_km) {
						frappe.throw("End Km is Mandatory")
					}
					else if (!data.total_km) {
						frappe.throw("Total Km is Mandatory")
					}
					else {
						frappe.call({
							method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.create_checkout",
							args: {
								end_km: data.end_km,
								total_km: data.total_km
							},
							callback(r) {
								if (r.message) {
									frappe.show_alert({ "message": "CheckOut Created Successfully", "indicator": "green" })
								}
								else {
									frappe.show_alert({ "message": "<p>Failed to Create CheckOut</p>", "indicator": "red" })
								}
								dialog.hide()
							}
						})
					}
				}
			})
			frappe.call({
				method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.validate_checkout",
				callback(r) {
					if (r.message) {
						dialog.show()
					}
				}
			})
		})
	},
	date: function (frm) {
		if (frm.doc.date) {
			(frm.doc.for_doctor_and_dealer || []).concat(frm.doc.for_customer || []).forEach(row => {
				let cdt = row.doctype, cdn = row.name;
				if (row.customer) {
					frappe.call({
						method: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.get_customer_order_ids_and_values',
						args: {
							customer: row.customer,
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
	for_doctor_and_dealer_add: function (frm) {
		let data = locals[cdt][cdn];
		frm.fields_dict.for_doctor_and_dealer.grid.grid_rows[data.idx - 1].make_control(frm.fields_dict.for_doctor_and_dealer.grid.grid_rows[data.idx - 1].columns.create)
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
				fieldtype: "Check",
				default: 1,
				onchange: function () {
					if (cur_dialog.get_field("sales_order").get_value()) {
						cur_dialog.get_field("payment_entry").set_value(0);
					} else if (!cur_dialog.get_field("payment_entry").get_value()) {
						cur_dialog.get_field("sales_order").set_value(1);
					}
				}
			},
			{
				fieldtype: 'Column Break'
			},
			{
				fieldname: "payment_entry",
				label: __("Payment Entry"),
				fieldtype: "Check",
				onchange: function () {
					if (cur_dialog.get_field("payment_entry").get_value()) {
						cur_dialog.get_field("sales_order").set_value(0);
					} else if (!cur_dialog.get_field("sales_order").get_value()) {
						cur_dialog.get_field("payment_entry").set_value(1);
					}
				}
			},
		],
		primary_action_label: __("Create"),
		primary_action: function (data) {
			let row = locals[cdt][cdn]
			if (data.sales_order) {
				frappe.new_doc('Sales Order', { 'customer': row.customer });
			} else if (data.payment_entry) {
				frappe.new_doc('Payment Entry', {
					'payment_type': 'Receive',
					'party_type': 'Customer',
					'party': row.customer,
				}).then(() => {
					cur_frm.set_value('party', row.customer);
				});
			} else {
				frappe.msgprint('Please choose either <b>Sales Order</b> or <b>Payment Entry</b>', __('Value Missing'));
			}
		}
	});

	d.show();
}
