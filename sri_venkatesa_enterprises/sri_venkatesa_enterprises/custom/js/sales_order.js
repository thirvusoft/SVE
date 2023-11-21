frappe.ui.form.on("Sales Order", {
    refresh: function(frm){
        setTimeout(()=>{
            frm.remove_custom_button("Purchase Order", "Create")
            frm.remove_custom_button("Material Request", "Create")
            frm.remove_custom_button("Pick List", "Create")
            frm.remove_custom_button("Work Order", "Create")
            frm.remove_custom_button("Request for Raw Materials", "Create")
            frm.remove_custom_button("Project", "Create")
            frm.remove_custom_button("Subscription", "Create")
            frm.remove_custom_button("Payment Request", "Create")
        }, 200)
    }
    
})