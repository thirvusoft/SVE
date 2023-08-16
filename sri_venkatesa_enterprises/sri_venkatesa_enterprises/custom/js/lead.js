frappe.ui.form.on("Lead", {
    refresh: function(frm){
        sve.farm.clear_farm(frm);
        if(!frm.is_new()){
            frappe.call({
                method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.get_farm_list",
                args:{
                    ref_doctype:frm.doc.doctype,
                    ref_name:frm.doc.name
                },
                callback(r){
                    frm.doc.__onload["farm_list"] = r.message
                    sve.farm.render_farm(frm)
                }
            })
        }
    }
})