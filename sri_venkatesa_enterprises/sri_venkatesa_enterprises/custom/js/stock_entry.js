frappe.ui.form.on("Stock Entry", {
    refresh: function(frm){
        setTimeout(()=>{
            frm.remove_custom_button("Expired Batches", "Get Items From")
            frm.remove_custom_button("Bill of Materials", "Get Items From")
            frm.remove_custom_button("Transit Entry", "Get Items From")
        }, 200)
    }
})