
from frappe import _
import frappe


def validate_lead_approval(doc,event):
	if doc.opportunity_from == "Lead":
		lead_doc=frappe.get_doc("Lead",doc.party_name)
		if lead_doc.workflow_state != "Approved":
			frappe.throw(_("Lead is not Approved"))