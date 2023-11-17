frappe.ui.form.on("Item Group", {
    refresh: function (frm) {
            frm.set_query("item", "custom_incentive", () => {
                return {
                    filters: {
                        "item_group": frm.doc.name
                    }
                }
            })
    }
});