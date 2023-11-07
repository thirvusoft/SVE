frappe.ui.form.on("Payment Entry", {
    refresh: function(frm){
        if(frm.is_new()){
            frm.trigger("payment_type")
        }
    },
    payment_type: function(frm){
        if(frm.doc.payment_type == "Pay"){
            frm.set_value("party_type", "Supplier")
        }
        else if(frm.doc.payment_type == "Receive"){
            frm.set_value("party_type", "Customer")
        }
    }
})