frappe.ui.form.on("Purchase Invoice", {
    refresh: function(frm){
		frm.set_query('custom_transporter', function() {
			return {
				filters: {
					'is_transporter': 1
				}
			}
		});
    }
})