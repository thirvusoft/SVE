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
          var farm = frappe.model.get_new_doc("Farm Details");
          farm[frappe.scrub(frm.doc.doctype)] = frm.doc.name;
          frappe.ui.form.make_quick_entry("Farm Details", void 0, void 0, farm);
        });
      }
    }
  });

  // frappe-html:/home/frappe/frappe-bench/apps/sri_venkatesa_enterprises/sri_venkatesa_enterprises/public/js/sve/farm_list.html
  frappe.templates["farm_list"] = `<div class="clearfix"></div>
{% for(var i=0, l=farm_list.length; i<l; i++) { %}
<div class="address-box">
	<p class="h6">
		{%= i+1 %}.
		<a href="/app/farm-details/{%= encodeURIComponent(farm_list[i].name) %}" class="btn btn-default btn-xs pull-right"
			style="margin-top:-3px; margin-right: -5px;">
			{%= __("Edit") %}</a>
	</p>
	<p>{%= farm_list[i].display %}</p>
</div>
{% } %}
{% if(!farm_list.length) { %}
<p class="text-muted small">{%= __("No Farm added yet.") %}</p>
{% } %}
<p><button class="btn btn-xs btn-default btn-address">{{ __("New Farm") }}</button></p>`;
})();
//# sourceMappingURL=sve.bundle.653UU4AH.js.map
