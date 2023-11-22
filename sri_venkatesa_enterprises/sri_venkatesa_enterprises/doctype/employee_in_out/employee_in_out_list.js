frappe.listview_settings["Employee In Out"] = {
    onload: function(list_view){
        list_view.page.add_inner_button(__("Checkin"), function(){
            let dialog = new frappe.ui.Dialog({
                title:"Enter Start Km",
                fields:[
                    {fieldname:"start_km", label:"Start Km", fieldtype:"Float", reqd:1},
                    {fieldtype:"Column Break"},
                    {fieldname:"vehicle_used", label:"Vehicle Used", fieldtype:"Link", reqd:1, options:"Employee Vehicle Type", default:"BIKE"}
                ],
                primary_action(data){
                    if(!data.start_km){
                        frappe.throw("Start Km is Mandatory")
                    }
                    else{
                        frappe.call({
                            method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.create_checkin",
                            args:{
                                start_km:data.start_km,
                                vehicle_used:data.vehicle_used
                            },
                            callback(r){
                                if(r.message){
                                    frappe.show_alert({"message":"Checkin Created Successfully", "indicator":"green"})
                                }
                                else{
                                    frappe.show_alert({"message":"<p>Failed to Create Checkin</p><p>Click on <b>Add Employee In Out</b> to create checkin</p>", "indicator":"red"})
                                }
                                dialog.hide()
                                list_view.refresh()
                            }
                        })
                    }
                }
            })
            dialog.show()
            
        })

        list_view.page.add_inner_button(__("Checkout"), function(){
            let dialog = new frappe.ui.Dialog({
                title:"Enter End Km",
                fields:[
                    {fieldname:"end_km", label:"End Km", fieldtype:"Float", reqd:1},
                    {fieldname:"total_km", label:"Total Km", fieldtype:"Float", reqd:1}
                ],
                primary_action(data){
                    if(!data.end_km){
                        frappe.throw("End Km is Mandatory")
                    }
                    else if(!data.total_km){
                        frappe.throw("Total Km is Mandatory")
                    }
                    else{
                        frappe.call({
                            method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.create_checkout",
                            args:{
                                end_km:data.end_km,
                                total_km:data.total_km
                            },
                            callback(r){
                                if(r.message){
                                    frappe.show_alert({"message":"CheckOut Created Successfully", "indicator":"green"})
                                }
                                else{
                                    frappe.show_alert({"message":"<p>Failed to Create CheckOut</p>", "indicator":"red"})
                                }
                                dialog.hide()
                                list_view.refresh()
                            }
                        })
                    }
                }
            })
            frappe.call({
                method:"sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.employee_in_out.employee_in_out.validate_checkout",
                callback(r){
                    if(r.message){
                        dialog.show()
                    }
                }
            })            
        })

    list_view.page.menu_btn_group.prevObject[0].style.marginTop="auto"
    $(list_view.page.menu_btn_group.prevObject.find(".custom-actions")).removeClass("hidden-xs")
    $(list_view.page.menu_btn_group.prevObject.find(".custom-actions")).removeClass("hidden-md")
    }
}