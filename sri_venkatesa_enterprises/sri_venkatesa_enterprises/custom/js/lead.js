frappe.ui.form.on("Lead", {
    refresh: function (frm) {
        frm.trigger('fill_location_on_save');
        frm.trigger("setup_new_sub_route")
        sve.farm.clear_farm(frm);
        setTimeout(()=>{ if(frm.doc.workflow_state!="Approved"){
            console.log("dgdfgfdg")
            frm.remove_custom_button("Customer","Create")
            frm.remove_custom_button("Quotation","Create")
            frm.remove_custom_button("Opportunity","Create")
            
        }
        },200)
        if (!frm.is_new()) {
            frappe.call({
                method: "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.get_farm_list",
                args: {
                    ref_doctype: frm.doc.doctype,
                    ref_name: frm.doc.name
                },
                callback(r) {
                    frm.doc.__onload["farm_list"] = r.message
                    sve.farm.render_farm(frm)
                }
            })
        }

        frm.set_query("from_dealer", () => {
            return {
                filters: {
                    "dealer": 1
                }
            }
        })
        frm.set_query("territory", () => {
            return {
                filters: {
                    "is_group": 1
                }
            }
        })
        frm.set_query("sub_route", () => {
            return {
                filters: {
                    "parent_territory": frm.doc.territory
                }
            }
        })
    },
    fill_location_on_save: function (frm) {
        if (frm.doc.latitude && frm.doc.longitude) {
            frm.fields_dict.location.map.setView([frm.doc.latitude, frm.doc.longitude], 13)
        }
        if (!frappe.flags.lead_save_overrided) {
            let save = frm.save;
            frm.save = async (...args) => {
                await frm.trigger("fill_location");
                save.call(frm, ...args);
            }
            frappe.flags.lead_save_overrided = true;
        }
    },
    fill_location: async function (frm) {
        frm.trigger("check_location_permission");
        async function getLocation() {
            try {
                let position = await new Promise((resolve, reject) => {
                    navigator.geolocation.getCurrentPosition(resolve, reject);
                });

                frm.doc.latitude = position.coords.latitude;
                frm.doc.longitude = position.coords.longitude;
                if (frm.doc.latitude && frm.doc.longitude) {
                    frm.fields_dict.location.map.setView([frm.doc.latitude, frm.doc.longitude], 13)
                }
                // You can use the latitude and longitude for your application here
            } catch (error) {
                // Handle errors by displaying them as alerts
                switch (error.code) {
                    case error.PERMISSION_DENIED:
                        window.alert("User denied the request for Geolocation.");
                        break;
                    case error.POSITION_UNAVAILABLE:
                        window.alert("Location information is unavailable.");
                        break;
                    case error.TIMEOUT:
                        window.alert("The request to get user location timed out.");
                        break;
                    default:
                        window.alert("An unknown error occurred.");
                }
            }
        }
        await getLocation();
    },
    check_location_permission: function (frm) {
        if ("geolocation" in navigator) {
            // Geolocation is available
        } else {
            // Geolocation is not available
            window.alert("Geolocation is not supported in this browser.");
        }
    },
    territory: function (frm) {
        frm.set_query("sub_route", () => {
            return {
                filters: {
                    "parent_territory": frm.doc.territory,
                    "is_group": 0
                }
            }
        })
    },
    setup_new_sub_route: function (frm) {
        let sub_route_field = frm.get_docfield("sub_route");
        sub_route_field.get_route_options_for_new_doc = function (frm) {
            return {
                "parent_territory": frm.doc.territory
            };
        };
    },
})
