from . import __version__ as app_version

app_name = "sri_venkatesa_enterprises"
app_title = "Sri Venkatesa Enterprises"
app_publisher = "Thirvusoft"
app_description = "Sri Venkatesa Enterprises"
app_email = "info@thirvusoft.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
app_include_css = "/assets/sri_venkatesa_enterprises/css/sve.css"
app_include_js = [
    "sve.bundle.js"
]

# include js, css files in header of web template
# web_include_css = "/assets/sri_venkatesa_enterprises/css/sri_venkatesa_enterprises.css"
# web_include_js = "/assets/sri_venkatesa_enterprises/js/sri_venkatesa_enterprises.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sri_venkatesa_enterprises/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Customer" : "sri_venkatesa_enterprises/custom/js/customer.js",
    "Lead" : "sri_venkatesa_enterprises/custom/js/lead.js",
    "Opportunity":"sri_venkatesa_enterprises/custom/js/opportunity.js",
    "Quotation": "sri_venkatesa_enterprises/custom/js/quotation.js",
    "Sales Invoice":"sri_venkatesa_enterprises/custom/js/sales_invoice.js",
    "Stock Entry":"sri_venkatesa_enterprises/custom/js/stock_entry.js",
    "Sales Order":"sri_venkatesa_enterprises/custom/js/sales_order.js",
    "Payment Entry":"sri_venkatesa_enterprises/custom/js/payment_entry.js",
    "Item Group":"sri_venkatesa_enterprises/custom/js/item_group.js",
    "Purchase Invoice":"sri_venkatesa_enterprises/custom/js/purchase_invoice.js"
    }
doctype_list_js = {
        "Sales Invoice" : "sri_venkatesa_enterprises/custom/js/sales_invoice_list.js",
        "Employee Checkin" : "sri_venkatesa_enterprises/custom/js/employee_checkin_list.js"
    }   
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
jinja = {
	"methods": [
        "frappe.contacts.doctype.address.address.get_default_address",
        "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.print_format_salesinvoice.get_invoice_item_and_tax_details"
    ]
#	"filters": "sri_venkatesa_enterprises.utils.jinja_filters"
 }

# Installation
# ------------

after_install = "sri_venkatesa_enterprises.after_install.after_install"
# after_migrate = "sri_venkatesa_enterprises.after_install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sri_venkatesa_enterprises.uninstall.before_uninstall"
# after_uninstall = "sri_venkatesa_enterprises.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "sri_venkatesa_enterprises.utils.before_app_install"
# after_app_install = "sri_venkatesa_enterprises.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "sri_venkatesa_enterprises.utils.before_app_uninstall"
# after_app_uninstall = "sri_venkatesa_enterprises.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sri_venkatesa_enterprises.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	# "Quotation": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.selling_controller.TsSellingController",
    "Sales Invoice": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.selling_controller.TsSellingController",
    "Sales Order": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.selling_controller.TsSalesOrderSellingController",
    # "Delivery Note": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.selling_controller.TsSellingController",
    "Employee":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee.TsEmployeeName",
    "Customer":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.TSCustomer",
    "Note":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.note.TSNote",
    "Salary Slip":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.salary_slip.TSSalarySlip"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Customer":{
        "after_insert" : ["sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.maintance_contact_details",
                          "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.set_exisiting_farm"
                          ],
        "validate" : ["sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.maintance_contact_details",
                      "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.set_exisiting_farm"
                      ],
        "on_update": [
            "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.customer.create_farm"
        ]
    },
    "Item":{
        "after_insert":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.item.update_price",
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.item.validate"
    },
    "Sales Invoice" : {
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_return.validate_return",
        "autoname":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_invoice.autoname",
    },
    "Delivery Note" : {
        "validate" : "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.delivery_return.validate_return"
    },
    "Lead":{
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.lead.validate"
    },
    "Quotation":{
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.quotation.validate_lead_approval"
    },
    "Opportunity":{
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.opportunity.validate",
        "after_insert":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.opportunity.appointment_payment_todo"
    },
    "GL Entry": {
        "on_submit": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.update_outstanding_amount"
    },
    "Sales Order": {
        "on_change": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.update_order_details",
        "after_delete": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.doctype.daily_activity.daily_activity.update_order_details",
        "validate": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_order.on_submit"
    },
    # 'Employee Checkin':{
    #     "validate": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee_checkin.create_expense_claim"
    # },
    "Employee":{
        "validate":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee.ssa_creation",
        "after_insert":"sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee.ssa_creation_afterinsert"
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "0 2 * * *": "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.opportunity.make_notification"
    },
    "daily": [
        "sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.employee.remind_employees_on_insurance_expiry"
    ]
}

# Testing
# -------

# before_tests = "sri_venkatesa_enterprises.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "sri_venkatesa_enterprises.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "sri_venkatesa_enterprises.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sri_venkatesa_enterprises.utils.before_request"]
# after_request = ["sri_venkatesa_enterprises.utils.after_request"]

# Job Events
# ----------
# before_job = ["sri_venkatesa_enterprises.utils.before_job"]
# after_job = ["sri_venkatesa_enterprises.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"sri_venkatesa_enterprises.auth.validate"
# ]
