import frappe

__version__ = '0.0.1'

def get_user_details(user=None):
    if not user:
        user = frappe.session.user
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

def get_travel_expense(start_date, end_date, employee):
    return frappe.db.sql(
        f"""
        select sum(chkn.total_km * veh.allowance_per_km) as allowance
        from `tabEmployee Checkin` chkn
        Left outer join `tabEmployee Vehicle Type` veh
            on chkn.vehicle_used = veh.name
        where employee = "{employee}" and time between "{start_date}" and "{end_date}"
        """
    )[0][0]
