erpnext.selling.CustomQuotationController = class CustomQuotationController extends erpnext.selling.QuotationController {
    make_sales_order() {
		var me = this;

		let has_alternative_item = this.frm.doc.items.some((item) => item.is_alternative);
		if (has_alternative_item) {
			this.show_alternative_items_dialog();
		} else if(cur_frm.doc.quotation_to == "Lead"){
            frappe.call({
                method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.quotation.check_linked_customer_with_lead",
                args:{
                    lead_name:cur_frm.doc.party_name
                },
                callback(r){
                    if(!r.message){
                        me.create_customer_dialog()
                    }
                    else{
                        frappe.model.open_mapped_doc({
                            method: "erpnext.selling.doctype.quotation.quotation.make_sales_order",
                            frm: me.frm
                        });
                    }
                }
            })
			
		}
        else{
            frappe.model.open_mapped_doc({
                method: "erpnext.selling.doctype.quotation.quotation.make_sales_order",
                frm: me.frm
            });
        }
	}
    create_customer_dialog(){
        var d = new frappe.ui.Dialog({
            title:"New Customer<br><p class='help-box small text-muted'>Customer not found for this Lead</p>",
            fields:[
                {fieldname:"customer_group", label:"Customer Group", fieldtype:"Link", options:"Customer Group", reqd:1},
                {fieldname:"col_brk_1", label:"", fieldtype:"Column Break"},
                {fieldname:"territory", label:"Territory", fieldtype:"Link", options:"Territory", reqd:1}
            ],
            primary_action_label:"Create Sales Order",
            primary_action: function(data){
                frappe.call({
                    method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.quotation.make_customer_from_lead",
                    args:{
                        source_name:cur_frm.doc.name,
                        customer_fields:data
                    },
                    callback(r){
                        frappe.model.open_mapped_doc({
                            method: "erpnext.selling.doctype.quotation.quotation.make_sales_order",
                            frm: me.frm
                        });
                    }
                })
            }
        })
        d.show()
    }
}
cur_frm.script_manager.make(erpnext.selling.CustomQuotationController); 