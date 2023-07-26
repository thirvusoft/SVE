from . import __version__ as app_version

app_name = "sve"
app_title = "Sri Venkatesa Enterprises"
app_publisher = "info@thirvusoft.in"
app_description = "Sri Venkatesa Enterprises"
app_email = "info@thirvusoft.in"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/sve/css/sve.css"
# app_include_js = "/assets/sve/js/sve.js"

# include js, css files in header of web template
# web_include_css = "/assets/sve/css/sve.css"
# web_include_js = "/assets/sve/js/sve.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "sve/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
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
# jinja = {
#	"methods": "sve.utils.jinja_methods",
#	"filters": "sve.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "sve.install.before_install"
after_install = "sve.after_install.after_install",
after_migrate = "sve.after_install.after_install"

# Uninstallation
# ------------

# before_uninstall = "sve.uninstall.before_uninstall"
# after_uninstall = "sve.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "sve.notifications.get_notification_config"

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

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }
doc_events = {
    "Customer":{
        "after_insert" : ["sve.sri_venkatesa_enterprises.custom.py.customer.maintance_contact_details",
                          "sve.sri_venkatesa_enterprises.custom.py.customer.set_exisiting_farm"
                          ],
        "validate" : ["sve.sri_venkatesa_enterprises.custom.py.customer.maintance_contact_details",
                      "sve.sri_venkatesa_enterprises.custom.py.customer.set_exisiting_farm"
                      ]
    },
    "Item":{
        "validate":"sve.sri_venkatesa_enterprises.custom.py.item.update_price"
    },
    "Sales Invoice" : {
        "validate" :"sve.sri_venkatesa_enterprises.custom.py.sales_return.validate_return"
    },
    "Delivery Note" : {
        "validate" : "sve.sri_venkatesa_enterprises.custom.py.delivery_return.validate_return"
    },
    "Lead":{
        "validate":"sve.sri_venkatesa_enterprises.custom.py.lead.sales_person_assign"
    }
}
# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"sve.tasks.all"
#	],
#	"daily": [
#		"sve.tasks.daily"
#	],
#	"hourly": [
#		"sve.tasks.hourly"
#	],
#	"weekly": [
#		"sve.tasks.weekly"
#	],
#	"monthly": [
#		"sve.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "sve.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "sve.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "sve.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["sve.utils.before_request"]
# after_request = ["sve.utils.after_request"]

# Job Events
# ----------
# before_job = ["sve.utils.before_job"]
# after_job = ["sve.utils.after_job"]

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
#	"sve.auth.validate"
# ]
