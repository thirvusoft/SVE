import frappe
import json
from frappe import _
@frappe.whitelist()
def check_linked_customer_with_lead(lead_name=None):
    if not lead_name:
        return True
    return frappe.db.exists("Customer", {"lead_name":lead_name})


@frappe.whitelist()
def make_customer_from_lead(source_name, ignore_permissions=False, customer_fields={}):
	if isinstance(customer_fields, str):
		customer_fields = json.loads(customer_fields)
	quotation = frappe.db.get_value(
		"Quotation", source_name, ["order_type", "party_name", "customer_name"], as_dict=1
	)

	if quotation and quotation.get("party_name"):
		if not frappe.db.exists("Customer", quotation.get("party_name")):
			lead_name = quotation.get("party_name")
			customer_name = frappe.db.get_value(
				"Customer", {"lead_name": lead_name}, ["name", "customer_name"], as_dict=True
			)
			if not customer_name:
				from erpnext.crm.doctype.lead.lead import _make_customer

				customer_doclist = _make_customer(lead_name, ignore_permissions=ignore_permissions)
				customer = frappe.get_doc(customer_doclist)
				for i in customer_fields:
					customer.update({i:customer_fields[i]})
				customer.flags.ignore_permissions = ignore_permissions
				if quotation.get("party_name") == "Shopping Cart":
					customer.customer_group = frappe.db.get_value(
						"E Commerce Settings", None, "default_customer_group"
					)

				try:
					customer.insert()
					return customer
				except frappe.NameError:
					if frappe.defaults.get_global_default("cust_master_name") == "Customer Name":
						customer.run_method("autoname")
						customer.name += "-" + lead_name
						customer.insert()
						return customer
					else:
						raise
				except frappe.MandatoryError as e:
					mandatory_fields = e.args[0].split(":")[1].split(",")
					mandatory_fields = [customer.meta.get_label(field.strip()) for field in mandatory_fields]

					frappe.local.message_log = []
					lead_link = frappe.utils.get_link_to_form("Lead", lead_name)
					message = (
						_("Could not auto create Customer due to the following missing mandatory field(s):") + "<br>"
					)
					message += "<br><ul><li>" + "</li><li>".join(mandatory_fields) + "</li></ul>"
					message += _("Please create Customer from Lead {0}.").format(lead_link)

					frappe.throw(message, title=_("Mandatory Missing"))
			else:
				return customer_name
		else:
			return frappe.get_doc("Customer", quotation.get("party_name"))



def validate_lead_approval(doc,event):
	if doc.quotation_to == "Lead":
		lead_doc=frappe.get_doc("Lead",doc.party_name)
		if lead_doc.workflow_state != "Approved":
			frappe.throw(_("Lead is not Approved"))
