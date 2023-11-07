import frappe

from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def employee_custom_fields():
    df = {
        "HR Settings": [
            dict(
                fieldname="vehicle_insurance_alert_section",
                label="Vehicle Insurance Expiry Alert",
                fieldtype="Section Break",
                insert_after="retirement_age",
            ),
            dict(
                fieldname="days_before_insurance_expiry_for_alert",
                label="Days to alert Employees before Vehicle Insurance Expiry Date",
                fieldtype="Int",
                description="In days",
                insert_after="vehicle_insurance_alert_section",
                default=60
            ),
            
            dict(
                fieldname="insurance_expiry_alert_role",
                label="Role to Send Vehicle Insurance Expiry Alert",
                fieldtype="Link",
                insert_after="days_before_insurance_expiry_for_alert",
                default="SVE Admin",
                options="Role",
                description="Select Role set to Admin User"
            ),
            dict(
                fieldname="employee_template",
                label="Alert Template for Employee",
                fieldtype="Link",
                insert_after="days_before_insurance_expiry_for_alert",
                options="Email Template"
            ),
            dict(
                fieldname="admin_template",
                label="Alert Template for Admin User",
                fieldtype="Link",
                insert_after="days_before_insurance_expiry_for_alert",
                options="Email Template"
            ),
        ]
    }
    create_custom_fields(df)