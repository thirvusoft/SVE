import frappe

def on_submit(doc,action):
    if not doc.sales_person_contribution: 
        sales_person = frappe.get_value("Sales Person",{"employee":frappe.get_value("Employee",{"user_id":frappe.session.user,"status":"Active"},"name"),"enabled":1},"name")
        doc.append("sales_person_contribution",dict(
            sales_person = sales_person,
            contribution = 100
        ))
