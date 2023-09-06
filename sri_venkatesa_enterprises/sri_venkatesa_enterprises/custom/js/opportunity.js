frappe.ui.form.on("Opportunity", {
    refresh: function(frm){
        var options = {
            enableHighAccuracy: true,
            timeout: 5000,
            maximumAge: 0,
          };
          
          function success(pos) {
            var crd = pos.coords;
          
            console.log("Your current position is:");
            console.log(`Latitude : ${crd.latitude}`);
            console.log(`Longitude: ${crd.longitude}`);
            console.log(`More or less ${crd.accuracy} meters.`);
            frappe.call({
                method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.lead.log_location",
                args:{msg:{
                    lat:crd.latitude,
                    long:crd.longitude,
                    accuracy:crd.accuracy
                }}
            })
          }
          
          function error(err) {
            console.warn(`ERROR(${err.code}): ${err.message}`);
          }
          
        //   navigator.geolocation.getCurrentPosition(success, error, options);
          
        frm.trigger("setup_new_sub_route")
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
        frm.set_query("territory", ()=>{
            return {
                filters:{
                    "is_group":1
                }
            }
        })
        frm.set_query("sub_route", ()=>{
            return {
                filters:{
                    "parent_territory":frm.doc.territory
                }
            }
        })
    },
    territory: function(frm){
        frm.set_query("sub_route", ()=>{
            return {
                filters:{
                    "parent_territory":frm.doc.territory,
                    "is_group":0
                }
            }
        })
    },
    setup_new_sub_route: function(frm) {
		let sub_route_field = frm.get_docfield("sub_route");
		sub_route_field.get_route_options_for_new_doc = function(frm) {
			return  {
				"parent_territory":frm.doc.territory
			};
		};
	},
})

frappe.ui.form.on("Follow Ups",{
    follow_up_add: function(frm, cdt, cdn){
        frappe.model.set_value(cdt, cdn, "followed_by", frappe.session.user)
        frappe.model.set_value(cdt, cdn, "next_followup_by", frappe.session.user)
        frappe.model.set_value(cdt, cdn, "date", frappe.datetime.nowdate() )
    }
})