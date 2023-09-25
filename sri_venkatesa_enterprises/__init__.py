__version__ = '0.0.1'
import frappe

def get_user_details(user=frappe.session.user):
    ret_dict = frappe._dict()
    ret_dict.update({
        "employee":frappe.db.get_value("Employee", {"user_id":user}, "name"),
        "employee_name":frappe.db.get_value("Employee", {"user_id":user}, "employee_name")
    })
    if(ret_dict.get("employee")):
        ret_dict.update({
            "sales_person":frappe.db.get_value("Sales Person", {"employee":ret_dict.employee, "enabled":1}, "name")
        })
    if(not ret_dict.get("sales_person")):
        ret_dict.update({
            "sales_person":frappe.db.get_value("Sales Person", {"employee":ret_dict.employee}, "name")
        })
    
    return ret_dict