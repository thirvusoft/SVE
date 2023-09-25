// Copyright (c) 2023, Thirvusoft and contributors
// For license information, please see license.txt

frappe.ui.form.on('Daily Activity', {
	refresh: function(frm) {
		frm.call({
			doc:frm.doc,
			method:"get_employee_id",
			callback(r){
				// frm.set_value("employee", r.message)
				frm.refresh_field("employee")
			}
		})
	}
});
