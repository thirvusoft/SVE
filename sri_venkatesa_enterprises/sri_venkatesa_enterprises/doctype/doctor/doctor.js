// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Doctor', {
	refresh: function(frm) {
		if(!frm.is_new()){
			frappe.contacts.render_address_and_contact(frm);
		}
	}
});
