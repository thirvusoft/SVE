frappe.provide("sve.farm");
console.log("SSS")
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
					frappe.ui.form.make_quick_entry("Farm Details", undefined, undefined, farm) 
				});
		}

	},
	// get_last_doc: function (frm) {
	// 	const reverse_routes = frappe.route_history.slice().reverse();
	// 	const last_route = reverse_routes.find((route) => {
	// 		return route[0] === "Form" && route[1] !== frm.doctype;
	// 	});
	// 	let doctype = last_route && last_route[1];
	// 	let docname = last_route && last_route[2];

	// 	if (last_route && last_route.length > 3) docname = last_route.slice(2).join("/");

	// 	return {
	// 		doctype,
	// 		docname,
	// 	};
	// },
	// get_address_display: function (frm, address_field, display_field) {
	// 	if (frm.updating_party_details) {
	// 		return;
	// 	}

	// 	let _address_field = address_field || "address";
	// 	let _display_field = display_field || "address_display";

	// 	if (!frm.doc[_address_field]) {
	// 		frm.set_value(_display_field, "");
	// 		return;
	// 	}

	// 	frappe
	// 		.xcall("frappe.contacts.doctype.address.address.get_address_display", {
	// 			address_dict: frm.doc[_address_field],
	// 		})
	// 		.then((address_display) => frm.set_value(_display_field, address_display));
	// },
});
