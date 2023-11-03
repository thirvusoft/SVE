frappe.ui.form.on("Sales Invoice", {
    refresh: function(frm){
        frm.set_query("shipping_adress_name", ()=>{
            return {
				query: 'frappe.contacts.doctype.address.address.address_query',
				filters: {
					link_doctype: "Farm Details",
					party_name: frm.doc.customer
				}
			};
        })
		setTimeout(()=>{
			frm.remove_custom_button("Fetch Timesheet");
			frm.remove_custom_button("Dunning","Create");
			frm.remove_custom_button("Subscription","Create");
			frm.remove_custom_button("Maintenance Schedule","Create");
			frm.remove_custom_button("Payment Request","Create");
			frm.remove_custom_button("Invoice Discounting","Create");
		},250)
    }
})

erpnext.accounts.TSSalesInvoiceController = class TSSalesInvoiceController extends erpnext.accounts.SalesInvoiceController {
    setup_queries() {
		var me = this;

		$.each([["customer", "customer"],
			["lead", "lead"]],
			function(i, opts) {
				if(me.frm.fields_dict[opts[0]])
					me.frm.set_query(opts[0], erpnext.queries[opts[1]]);
			});

		me.frm.set_query('contact_person', erpnext.queries.contact_query);
		me.frm.set_query('customer_address', erpnext.queries.address_query);
		me.frm.set_query("shipping_address_name", ()=>{
            return {
				query: 'sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_invoice.filter_farm_address',
				filters: {
					link_doctype: "Farm Details",
					party_name: me.frm.doc.customer
				}
			};
        })
		me.frm.set_query('dispatch_address_name', erpnext.queries.dispatch_address_query);

		erpnext.accounts.dimensions.setup_dimension_filters(me.frm, me.frm.doctype);

		if(this.frm.fields_dict.selling_price_list) {
			this.frm.set_query("selling_price_list", function() {
				return { filters: { selling: 1 } };
			});
		}

		if(this.frm.fields_dict.tc_name) {
			this.frm.set_query("tc_name", function() {
				return { filters: { selling: 1 } };
			});
		}

		if(!this.frm.fields_dict["items"]) {
			return;
		}

		if(this.frm.fields_dict["items"].grid.get_field('item_code')) {
			this.frm.set_query("item_code", "items", function() {
				return {
					query: "erpnext.controllers.queries.item_query",
					filters: {'is_sales_item': 1, 'customer': cur_frm.doc.customer, 'has_variants': 0}
				}
			});
		}

		if(this.frm.fields_dict["packed_items"] &&
			this.frm.fields_dict["packed_items"].grid.get_field('batch_no')) {
			this.frm.set_query("batch_no", "packed_items", function(doc, cdt, cdn) {
				return me.set_query_for_batch(doc, cdt, cdn)
			});
		}

		if(this.frm.fields_dict["items"].grid.get_field('item_code')) {
			this.frm.set_query("item_tax_template", "items", function(doc, cdt, cdn) {
				return me.set_query_for_item_tax_template(doc, cdt, cdn)
			});
		}

	}
}

extend_cscript(cur_frm.cscript, new erpnext.accounts.TSSalesInvoiceController({frm: cur_frm}));
