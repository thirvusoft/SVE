import frappe

def on_submit(doc,action):
    if len(doc.sales_person_contribution) == 0: 
        user = frappe.session.user
        if action == "Bulk Update":
            user = doc.owner 
        emp=frappe.get_value("Employee",{"user_id":user,"status":"Active"},"name")
        if not emp:
            return
        sales_person = frappe.get_value("Sales Person",{"employee":emp,"enabled":1},"name")
        if sales_person:
            doc.append("sales_person_contribution",dict(
                sales_person = sales_person,
                contribution = 100
            ))
            doc.calculate_contribution()
            if action == "Bulk Update":
                doc.flags.ignore_mandatory = True
                doc.save()

def update_all_sales_orders_sales_person_contribution():
    so = frappe.get_all("Sales Order",pluck="name")
    for i in so:
        so_update = frappe.get_doc("Sales Order",i)
        on_submit(so_update,"Bulk Update")