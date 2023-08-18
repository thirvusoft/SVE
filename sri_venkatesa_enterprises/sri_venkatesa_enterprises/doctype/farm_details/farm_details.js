// Copyright (c) 2023, info@thirvusoft.in and contributors
// For license information, please see license.txt

frappe.ui.form.on('Farm Details', {
	refresh: function(frm) {
		frappe.contacts.render_address_and_contact(frm);
	}
});
