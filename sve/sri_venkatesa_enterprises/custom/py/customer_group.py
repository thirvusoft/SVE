import frappe

def create_customer_group():  
    customer_group = ['Below 50','50 to 1L','1L to 1.5L','1.50 to 2','2 to 3','Above 3' ,'3 to 5','5 to 10']  
    for i in customer_group:
        if(not frappe.db.exists("Customer Group", i)):
            doc = frappe.new_doc("Customer Group")
            doc.customer_group_name = i
            doc.save(ignore_permissions=True)
        frappe.db.commit()