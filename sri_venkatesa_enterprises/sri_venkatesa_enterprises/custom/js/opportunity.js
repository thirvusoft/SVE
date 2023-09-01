frappe.ui.form.on("Opportunity", {
    refresh: function(frm){
        sve.farm.clear_farm(frm);
        if(!frm.is_new()){
            frappe.call({
                method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.get_farm_list",
                args:{
                    ref_doctype:frm.doc.opportunity_from,
                    ref_name:frm.doc.party_name
                },
                callback(r){
                    frm.doc.__onload["farm_list"] = r.message
                    sve.farm.render_farm(frm)
                }
            })
        }

        frm.set_query("from_dealer", ()=>{
            return {
                filters:{
                    "dealer":1
                }
            }
        })
    },
})

frappe.ui.form.on("Follow Ups",{
    follow_up_add: function(frm, cdt, cdn){
        frappe.model.set_value(cdt, cdn, "followed_by", frappe.session.user)
        frappe.model.set_value(cdt, cdn, "next_followup_by", frappe.session.user)
        frappe.model.set_value(cdt, cdn, "date", frappe.datetime.nowdate() )
    }
})