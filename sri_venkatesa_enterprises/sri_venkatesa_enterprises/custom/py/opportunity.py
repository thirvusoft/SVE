
from frappe import _
import frappe
import json
from frappe.utils import now_datetime, nowdate



def validate(doc, event=None):
	validate_lead_approval(doc)
	get_customer_details(doc)

def validate_lead_approval(doc):
	if doc.opportunity_from == "Lead":
		lead_doc=frappe.get_doc("Lead",doc.party_name)
		if lead_doc.workflow_state != "Approved":
			frappe.throw(_("Lead is not Approved"))

@frappe.whitelist()
def get_customer_details(doc):
	if isinstance(doc, str):
		doc=json.loads(doc)
	dl = frappe.db.get_value("Dynamic Link", {"parenttype":"Address", "link_doctype":doc.get("opportunity_from"), "link_name":doc.get("party_name")}, "parent")
	if dl:
		address = frappe.get_doc("Address", dl)
		doc.update({
			"city" : address.city,
			"state" : address.state
		})
	else:
		doc.update({
			"city" : "",
			"state" : ""
		})
	return {"city":doc.get("city"), "state":doc.get("state")}

def make_notification():
	oppor = frappe.get_all("Opportunity", filters={"next_follow_up":nowdate()}, fields=["name", "party_name", "next_follow_up", "remarks", "owner"])
	for i in oppor:
		doc=frappe.new_doc("Notification Log")
		doc.update({
			"document_name":i.name,
			"document_type":"Opportunity",
			"for_user": i.owner,
			"from_user": i.owner,
			"type": "Energy Point",
			"subject": f"Today's FollowUp: {i.party_name}",
			"email_content": f"<p>Remainder for Today's({i.next_follow_up}) Follow up</p><p>Party: {i.party_name}</p><p>{i.remarks}</p>"
		})
		doc.insert()