(() => {
  // ../sri_venkatesa_enterprises/sri_venkatesa_enterprises/public/js/sve/farm.js
  frappe.provide("sve.farm");
  console.log("SSS");
  $.extend(sve.farm, {
    clear_farm: function(frm) {
      $(frm.fields_dict["farm_html"].wrapper).html("");
    },
    render_farm: function(frm) {
      if (frm.fields_dict["farm_html"] && "farm_list" in frm.doc.__onload) {
        $(frm.fields_dict["farm_html"].wrapper).html(frappe.render_template("farm_list", frm.doc.__onload)).find(".btn-address").on("click", function() {
          frappe.new_doc("Farm Details");
        });
      }
    }
  });
})();
//# sourceMappingURL=farm.bundle.DYHRKETP.js.map
