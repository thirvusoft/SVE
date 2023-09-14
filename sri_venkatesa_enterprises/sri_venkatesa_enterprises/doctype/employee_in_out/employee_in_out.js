// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Employee In Out', {
	refresh: function(frm){
		if(frm.doc.start_km && frm.doc.end_km && !frm.is_dirty()){
			frm.set_df_property("start_km", "hidden", 1)
			frm.set_df_property("end_km", "hidden", 1)
		}
	},
	checkin: function(frm) {
		frm.set_value("checkin_time", frappe.datetime.now_datetime())
		if(frm.is_new()){
			frm.save()
		}
	},
	checkout: function(frm) {
		frm.set_value("checkout_time", frappe.datetime.now_datetime())
		frm.save()
	}
});
