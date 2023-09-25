frappe.ui.form.on("Sales Order", {
    refresh: function(frm){
        setTimeout(()=>{
            frm.remove_custom_button("Purchase Order", "Create")
            frm.remove_custom_button("Material Request", "Create")
           
        }, 200)
    }
})