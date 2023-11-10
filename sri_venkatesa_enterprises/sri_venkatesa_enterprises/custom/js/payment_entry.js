frappe.ui.form.on("Payment Entry", {
    refresh: function(frm){
        if(frm.is_new()){
            frm.trigger("payment_type")
        }
        if (!frm.doc.__islocal) {
            let r = cur_frm.add_custom_button("Generate QR", async function () {
              frappe.call({
                method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.payment_entry.set_qr_image",
                args:{
                    doc:frm.doc, 
                },
                callback(r){
                    frm.reload_doc()
                    if (r.message){
                        frappe.show_alert({message:"QR Generated Successfully", indicator:"green"})
                    }
                    else {
                        frappe.show_alert({message:"QR Generation Failed", indicator:"red"})
                    }
                }
              })
            })
            r[0].style.backgroundColor = "green" 
            r[0].style.color = "white"
          }
      
    },
    payment_type: function(frm){
        if(frm.doc.payment_type == "Pay"){
            frm.set_value("party_type", "Supplier")
        }
        else if(frm.doc.payment_type == "Receive"){
            frm.set_value("party_type", "Customer")
        }
    },

})