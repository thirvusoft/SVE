import frappe


def validate(doc, event=None):
    validate_mobile_no(doc)
    sales_person_assign(doc)

def sales_person_assign(doc):
    if doc.territory:
        sales_team_emp = {}
        doc_ = frappe.new_doc("ToDo")        
        if frappe.db.exists("ToDo", {'reference_name': doc.name}):
            doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name})
        user = frappe.db.get_value("User", doc.owner, "username")
        sales_team = frappe.get_doc("Territory", {'name': doc.territory},pluck="territory_manager")
        if sales_team.territory_manager:
            sales_team_emp = frappe.get_doc("Sales Person", {'name': sales_team.territory_manager},pluck="employee")
        if sales_team_emp and sales_team_emp.employee:
            emp_user = frappe.get_doc("Employee", {'name': sales_team_emp.employee},pluck="user_id")
        if not sales_team.territory_manager:
            frappe.msgprint("There is no sales person in territory")
        elif sales_team_emp and not sales_team_emp.employee:
            frappe.msgprint("There is no employee in sales Team ")
        elif not emp_user.user_id:
            frappe.msgprint("There is no user id in employee")
        else:
            doc_.update({
                'date': frappe.utils.nowdate(),
                'allocated_to': emp_user.user_id,
                'description': f'Assignment for {doc.doctype} {doc.name}',
                'reference_type': doc.doctype,
                'reference_name': doc.name,
                'assigned_by': user,
            })
            doc_.flags.ignore_permissions = True
            doc_.flags.ignore_links = True
            doc_.save()

def validate_mobile_no(doc):
    def throw(field):
        error_msg=f"""
        <p>{field} should be length of 10 Digits</p>
        <p>{field} should start either with 9 or 8 or 7 or 6</p>
        <p>{field} contains only numeric</p>
        """
        frappe.throw(title=f"{field} Validation Failed", msg=error_msg)
    if(doc.mobile_no):
        if len(doc.mobile_no) != 10 or doc.mobile_no[0] not in ["9", "8", "7", "6"]:
            throw("Mobile No")
    if(doc.whatsapp_no):
        if len(doc.whatsapp_no) != 10 or doc.whatsapp_no[0] not in ["9", "8", "7", "6"]:
            throw("Whatsapp No")


@frappe.whitelist()
def log_location(msg):
    frappe.log_error(msg)





def create_status():
    doc=frappe.new_doc('Property Setter')
    doc.update({
        "doctype_or_field": "DocField",
        "doc_type":"Lead",
        "field_name":"type",
        "property":"options",
        "value":"\nCustomer\nDoctor\nDealer"
    })
    doc.save()
    frappe.db.commit()