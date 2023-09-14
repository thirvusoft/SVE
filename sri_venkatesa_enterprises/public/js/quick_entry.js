frappe.ui.form.EmployeeInOutQuickEntryForm = class EmployeeInOutQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	}

	render_dialog() {
		var me = this;

		this.dialog = new frappe.ui.Dialog({
			title: __("New {0}", [__(this.doctype)]),
			fields: this.mandatory,
			doc: this.doc,
		});

		this.register_primary_action();
		!this.force && this.render_edit_in_full_page_link();
		// ctrl+enter to save
		this.dialog.wrapper.keydown(function (e) {
			if ((e.ctrlKey || e.metaKey) && e.which == 13) {
				if (!frappe.request.ajax_count) {
					// not already working -- double entry
					me.dialog.get_primary_btn().trigger("click");
					e.preventDefault();
					return false;
				}
			}
		});

		this.dialog.onhide = () => (frappe.quick_entry = null);
		this.dialog.show();
		this.dialog.fields_dict.checkin.onclick = function(){
			console.log("clicked")
			me.dialog.fields_dict.checkin_time.set_value(frappe.datetime.now_datetime()).then(()=>{
				me.dialog.refresh()
				me.dialog.get_primary_btn().click()
			})
			
		}
		this.dialog.refresh_dependency();
		this.set_defaults();

		if (this.init_callback) {
			this.init_callback(this.dialog);
		}
	}
}