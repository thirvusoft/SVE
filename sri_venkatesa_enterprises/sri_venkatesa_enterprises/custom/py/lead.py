import frappe

def sales_person_assign(doc,actions):
    if doc.territory:
        doc_ = frappe.new_doc("ToDo")        
        if frappe.db.exists("ToDo", {'reference_name': doc.name}):
            doc_ = frappe.get_doc("ToDo", {'reference_name': doc.name})
        user = frappe.db.get_value("User", doc.owner, "username")
        sales_team = frappe.get_doc("Territory", {'name': doc.territory},pluck="territory_manager")
        if sales_team.territory_manager:
            sales_team_emp = frappe.get_doc("Sales Person", {'name': sales_team.territory_manager},pluck="employee")
        if sales_team_emp.employee:
            emp_user = frappe.get_doc("Employee", {'name': sales_team_emp.employee},pluck="user_id")
        if not sales_team.territory_manager:
            frappe.msgprint("There is no sales person in territory")
        elif not sales_team_emp.employee:
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