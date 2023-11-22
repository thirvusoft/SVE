frappe.ui.form.on("Purchase Invoice", {
    
    refresh(frm){
        if (frm.doc.docstatus == 1){

            frm.add_custom_button(
                __('Landed Cost Voucher'),
                function() {open_landed_cost_voucher(frm)},
                __('Create')
            );
            
        }
    }
})

function open_landed_cost_voucher(frm){

    let lcv = frappe.model.get_new_doc('Landed Cost Voucher');
    lcv.company = frm.doc.company;
    lcv.posting_date = frm.doc.posting_date;

    let lcv_receipt = frappe.model.get_new_doc('Landed Cost Purchase Receipt');
    lcv_receipt.receipt_document_type = 'Purchase Invoice';
    lcv_receipt.receipt_document = frm.doc.name;
    lcv_receipt.supplier = frm.doc.supplier;
    lcv_receipt.grand_total = frm.doc.grand_total;
    lcv.purchase_receipts = [lcv_receipt];
    
    frappe.set_route("Form", lcv.doctype, lcv.name);

}