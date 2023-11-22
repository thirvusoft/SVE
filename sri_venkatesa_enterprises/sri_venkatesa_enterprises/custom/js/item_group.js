frappe.ui.form.on("Item Group", {
    refresh: function (frm) {
            frm.set_query("item", "custom_incentive", () => {
                return {
                    filters: {
                        "item_group": frm.doc.name
                    }
                }
            })
            frm.set_query("employee", "custom_incentive", () => {
                return {
                    filters: {
                        "custom_sales_person_type": "Employee"
                    }
                }
            })
            frm.set_query("item", "custom_doctor_commision", () => {
                return {
                    filters: {
                        "item_group": frm.doc.name
                    }
                }
            })
            frm.set_query("doctor", "custom_doctor_commision", () => {
                return {
                    filters: {
                        "custom_sales_person_type": "Doctor"
                    }
                }
            })
    }
});