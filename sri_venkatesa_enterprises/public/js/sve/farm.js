frappe.provide("sve.farm");
$.extend(sve.farm, {
	clear_farm: function (frm) {
		$(frm.fields_dict["farm_html"].wrapper).html("");
	},

	render_farm: function (frm) {
		// render farms
		if (frm.fields_dict["farm_html"] && "farm_list" in frm.doc.__onload) {
			$(frm.fields_dict["farm_html"].wrapper)
				.html(frappe.render_template("farm_list", frm.doc.__onload))
				.find(".btn-address")
				.on("click", function () {
					var farm = frappe.model.get_new_doc("Farm Details");
					farm[frappe.scrub(frm.doc.doctype) ]=frm.doc.name;
					if(frm.doc.doctype == "Opportunity"){
						farm[frappe.scrub(frm.doc.opportunity_from) ]=frm.doc.party_name;
					}
					frappe.ui.form.make_quick_entry("Farm Details", undefined, undefined, farm) 
				});
		}

	},
});
