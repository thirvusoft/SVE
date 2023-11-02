frappe.provide('frappe.ui.form');

frappe.ui.form.ContactAddressQuickEntryForm = class ContactAddressQuickEntryForm extends frappe.ui.form.QuickEntryForm {
	constructor(doctype, after_insert, init_callback, doc, force) {
		super(doctype, after_insert, init_callback, doc, force);
		this.skip_redirect_on_error = true;
	}

	render_dialog() {
		this.mandatory = this.mandatory.concat(this.get_variant_fields());
		super.render_dialog();
		this.dialog.set_value("country", "India")
		const state_field = this.dialog.get_field("state");
        const country = this.dialog.get_value("country");
        state_field.set_data(frappe.boot.india_state_options || []);
	}

	insert() {
		/**
		 * Using alias fieldnames because the doctype definition define "email_id" and "mobile_no" as readonly fields.
		 * Therefor, resulting in the fields being "hidden".
		 */
		const map_field_names = {
			"email_address": "email_id",
			"mobile_number": "mobile_no",
		};

		Object.entries(map_field_names).forEach(([fieldname, new_fieldname]) => {
			this.dialog.doc[new_fieldname] = this.dialog.doc[fieldname];
			delete this.dialog.doc[fieldname];
		});

		return super.insert();
	}

	get_variant_fields() {
		var variant_fields = [{
            fieldtype: 'Int',
            fieldname: 'batch_size',
            label: 'Batch Size'
        },
        {
			fieldtype: "Section Break",
			label: __("Contact Details"),
			collapsible: 1
		},
		{
			label: __("Email Id"),
			fieldname: "email_address",
			fieldtype: "Data",
			options: "Email",
		},
		{
			label: __("Designation"),
			fieldname: "designation",
			fieldtype: "Link",
			options: "Designation",
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("Mobile Number"),
			fieldname: "mobile_number",
			fieldtype: "Data",
			reqd:1
		},
		{
			fieldtype: "Section Break",
			label: __("Address Details"),
			collapsible: 1
		},
		{
			label: __("Door No/Street"),
			fieldname: "address_line1",
			fieldtype: "Data"
		},
		{
			label: __("Taluk/Mandal"),
			fieldname: "address_line2",
			fieldtype: "Data"
		},
		{
			label: __("ZIP Code"),
			fieldname: "pincode",
			fieldtype: "Data"
		},
		{
			label: __("Aadhar no"),
			fieldname: "aadhar_no",
			fieldtype: "Data"
		},
		{
			fieldtype: "Column Break"
		},
		{
			label: __("City"),
			fieldname: "city",
			fieldtype: "Data"
		},
		{
			label: __("District"),
			fieldname: "district",
			fieldtype: "Link",
			options:"District"
		},
		{
			label: __("State"),
			fieldname: "state",
			fieldtype: "Autocomplete"
		},
		{
			label: __("Country"),
			fieldname: "country",
			fieldtype: "Link",
			options: "Country"
		},
		{
			label: __("Customer POS Id"),
			fieldname: "customer_pos_id",
			fieldtype: "Data",
			hidden: 1
		}];

		return variant_fields;
	}
}

frappe.provide('frappe.ui.form');

frappe.ui.form.CustomerQuickEntryForm = frappe.ui.form.ContactAddressQuickEntryForm;
