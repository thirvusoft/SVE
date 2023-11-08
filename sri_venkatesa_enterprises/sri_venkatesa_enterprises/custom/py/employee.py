from erpnext.setup.doctype.employee.employee import Employee
import frappe
from frappe.model.naming import set_name_by_naming_series
from frappe.utils import get_url_to_form, now_datetime,strip_html_tags, today, add_days

def get_link_to_form(doctype: str, name: str, label: str | None = None) -> str:
	if not label:
		label = name

	return f"""<a href="{get_url_to_form(doctype, name)}" target="_blank">{label}</a>"""

class TsEmployeeName(Employee):
	def autoname(self):
		self.name = (self.first_name or "").strip() + " " + (self.last_name or "").strip()
		self.employee = self.name


def remind_employees_on_insurance_expiry():
	days_before = frappe.db.get_single_value("HR Settings", "days_before_insurance_expiry_for_alert")
	role_to_alert = frappe.db.get_single_value("HR Settings", "insurance_expiry_alert_role")
	if not role_to_alert:
		frappe.log_error(title="Error in Insurance Expiry Alert", message=f"""<b>Role to Send Vehicle Insurance Expiry Alert</b> not found in <b>HR Settings</b>""")
	employees = frappe.get_all("Employee", filters={"status":"Active"}, fields=["name", "user_id", "employee_name", "insurance_expiry_date", "insurance"])
	alerted_employees = []
	for i in employees:
		if not i.get("user_id"):
			frappe.log_error(title="Error in Insurance Expiry Alert", message=f"""<b>User Id</b> not found for Employee {get_link_to_form("Employee", i.get("name"))}""")
		if not i.get("insurance_expiry_date"):
			frappe.log_error(title="Error in Insurance Expiry Alert", message=f"""Vehicle Insurance Expiry Date not found for Employee {get_link_to_form("Employee", i.get("name"))}""")
			continue
		if exp_date:=i.get("insurance_expiry_date"):
			now_date = now_datetime().date()
			if((exp_date-now_date).days <= days_before):
				alerted_employees.append({"employee":i.get("name"),"employee_link":get_link_to_form("Employee", i.get("name")), "employee_name":i.get("employee_name"), "expiry_date":i.get("insurance_expiry_date").strftime("%d-%m-%Y"), "pending_days":(exp_date-now_date).days, "insurance_file":i["insurance"]})
				employee_insurance_expiry_note(employee = i)
	
	alert_admin_on_insurance_expiry(role_to_alert, alerted_employees)

def employee_insurance_expiry_note(employee):
	employee_doc = frappe.get_doc("Employee", employee)
	alert_template_for_emp = frappe.db.get_single_value("HR Settings", "employee_template")
	
	if not alert_template_for_emp:
		frappe.log_error(title="Error in Insurance Expiry Alert", message="<b>Alert Template for Employee</b> not found in <b>HR Settings</b>")
		return

	employee_alert_template = frappe.get_doc("Email Template", alert_template_for_emp)
	
	employee_message = frappe.render_template(employee_alert_template.response if(employee_alert_template.response and strip_html_tags(employee_alert_template.response)) else employee_alert_template.response_html, employee_doc.as_dict())
	other_users = frappe.get_all("User", filters={"enabled":1, "name":["!=", employee_doc.user_id]}, fields=["name as user"])
	if to_del:=frappe.db.get_all("Note", filters={"title": employee_alert_template.subject}, pluck="name"):
		frappe.delete_doc("Note", to_del)
	note = frappe.new_doc("Note")
	note.update({
		"title":employee_alert_template.subject,
		"public":1,
		"notify_on_login":1,
		"notify_on_every_login":0,
		"expire_notification_on":employee_doc.insurance_expiry_date,
		"content":employee_message,
		"seen_by":other_users,
	})
	note.insert()

def alert_admin_on_insurance_expiry(role_to_alert, employees=[]):
	if not employees:
		return
	alert_users = frappe.get_all("Has Role", filters={"parenttype":"User", "role":role_to_alert}, pluck="parent")
	alert_template_for_admin = frappe.db.get_single_value("HR Settings", "admin_template")
	if not alert_template_for_admin:
		frappe.log_error(title="Error in Insurance Expiry Alert", message="<b>Alert Template for Admin User</b> not found in <b>HR Settings</b>")
		return
	context = frappe._dict()
	for i in employees:
		context.update({
			i["employee"]:frappe._dict(i)
		})
	admin_alert_template = frappe.get_doc("Email Template", alert_template_for_admin)
	admin_message = frappe.render_template(admin_alert_template.response if(admin_alert_template.response and strip_html_tags(admin_alert_template.response)) else admin_alert_template.response_html, {"context":context})
	print(context)
	other_users = frappe.get_all("User", filters={"enabled":1, "name":["not in", alert_users]}, fields=["name as user"])
	if to_del:=frappe.db.get_all("Note", filters={"title":admin_alert_template.subject}, pluck="name"):
		frappe.delete_doc("Note", to_del)
	note = frappe.new_doc("Note")
	note.update({
		"title":admin_alert_template.subject,
		"public":1,
		"notify_on_login":1,
		"notify_on_every_login":0,
		"expire_notification_on": add_days(today(), 1),
		"content":admin_message,
		"seen_by":other_users,
	})
	note.insert()
 
def ssa_creation(doc,action):
	if not doc.get("__islocal"):
		ssa=frappe.db.get_all("Salary Structure Assignment", filters={"employee":doc.name, "salary_structure":["!=", doc.custom_salary_structure], 'docstatus': 1}, 
						fields=["name"])
		for ss in ssa:
			ssa_structure=frappe.get_doc("Salary Structure Assignment", ss.name)
			ssa_structure.cancel()
			ssa_structure.delete()

		if doc.custom_salary_structure:
			assignment=frappe.get_all("Salary Structure Assignment", {"employee":doc.employee, "salary_structure":doc.custom_salary_structure, 'docstatus': 1})
			if assignment:
				pass
			else:
				ssa_doc=frappe.new_doc("Salary Structure Assignment")
				ssa_doc.employee=doc.name
				ssa_doc.salary_structure=doc.custom_salary_structure
				ssa_doc.department=doc.department
				ssa_doc.designation=doc.designation
				ssa_doc.from_date=doc.date_of_joining
				ssa_doc.company=doc.company
				ssa_doc.save()
				ssa_doc.submit()
    
def ssa_creation_afterinsert(doc,action):
	ssa=frappe.db.get_all("Salary Structure Assignment", filters={"employee":doc.name, "salary_structure":["!=", doc.custom_salary_structure], 'docstatus': 1}, 
					fields=["name"])
	for ss in ssa:
		ssa_structure=frappe.get_doc("Salary Structure Assignment", ss.name)
		ssa_structure.cancel()
		ssa_structure.delete()

	if doc.custom_salary_structure:
		assignment=frappe.get_all("Salary Structure Assignment", {"employee":doc.employee, "salary_structure":doc.custom_salary_structure, 'docstatus': 1})
		if assignment:
			pass
		else:
			ssa_doc=frappe.new_doc("Salary Structure Assignment")
			ssa_doc.employee=doc.name
			ssa_doc.salary_structure=doc.custom_salary_structure
			ssa_doc.department=doc.department
			ssa_doc.designation=doc.designation
			ssa_doc.from_date=doc.date_of_joining
			ssa_doc.company=doc.company
			ssa_doc.save()
			ssa_doc.submit()