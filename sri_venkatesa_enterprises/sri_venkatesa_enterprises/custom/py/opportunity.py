
from frappe import _
import frappe
import json
from frappe.utils import now_datetime, nowdate



def validate(doc, event=None):
	validate_lead_approval(doc)
	get_customer_details(doc)
	if not doc.is_new():
		appointment_payment_todo(doc)
	
def validate_lead_approval(doc):
	if doc.opportunity_from == "Lead":
		lead_doc=frappe.get_doc("Lead",doc.party_name)
		if lead_doc.workflow_state != "Approved":
			frappe.throw(_("Lead is not Approved"))
			
def appointment_payment_todo(doc,event=None):
	if doc.next_follow_up:
		emp_user = frappe.get_doc("Employee", {'name':doc.custom_employee},pluck="user_id")
		if not emp_user.user_id:
			frappe.msgprint("There is no user id in employee")
		doc_ = frappe.new_doc("ToDo") 

		if frappe.db.exists("ToDo", {'reference_name': doc.name,'date':doc.next_follow_up}):
			doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name})
		else:
			doc_.update({
				'date': doc.next_follow_up,
				'allocated_to': emp_user.user_id,
				'description': f'Assignment for Appointment {doc.doctype} {doc.name}',
				'reference_type': doc.doctype,
				'reference_name': doc.name,
				'assigned_by': frappe.session.user,
			})
			doc_.flags.ignore_permissions = True
			doc_.flags.ignore_links = True
			doc_.insert()


	if doc.custom_payment_date:
		emp_user = frappe.get_doc("Employee", {'name':doc.custom_employee},pluck="user_id")
		if not emp_user.user_id:
			frappe.msgprint("There is no user id in employee")
		doc_ = frappe.new_doc("ToDo")        
		if frappe.db.exists("ToDo", {'reference_name': doc.name,'date':doc.custom_payment_date}):
			doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name})

		else:
			doc_.update({
				'date': doc.custom_payment_date,
				'allocated_to': emp_user.user_id,
				'description': f'Assignment for Payment Followup {doc.doctype} {doc.name}',
				'reference_type': doc.doctype,
				'reference_name': doc.name,
				'assigned_by': frappe.session.user,
			})
			doc_.flags.ignore_permissions = True
			doc_.flags.ignore_links = True
			doc_.save()

	


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
	payment_date = frappe.get_all("Opportunity", filters={"custom_payment_date":nowdate()}, fields=["name", "party_name", "custom_payment_date", "remarks", "owner"])
	for i in payment_date:
		doc=frappe.new_doc("Notification Log")
		doc.update({
			"document_name":i.name,
			"document_type":"Opportunity",
			"for_user": i.owner,
			"from_user": i.owner,
			"type": "Energy Point",
			"subject": f"Today's Payment FollowUp: {i.party_name}",
			"email_content": f"<p>Remainder for Today's({i.custom_payment_date}) Payment Follow up</p><p>Party: {i.party_name}</p><p>{i.remarks}</p>"
		})
		doc.insert()