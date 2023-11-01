import frappe
from frappe.utils import now_datetime, nowdate

def create_expense_claim(doc,event):
    if (doc.total_km or 0) > 0 and not doc.expense_claim:
        exp_clm = frappe.new_doc('Expense Claim')
        exp_clm.employee = doc.employee
        exp_clm.expense_approver = frappe.get_value('Employee',doc.employee,'expense_approver')
        company = frappe.get_value('Employee',doc.employee,'company')
        expense_type = frappe.get_value('Employee',doc.employee,'expense_type')
        if expense_type:
            exp_clm.append('expenses',{
                'expense_date':doc.time,
                'expense_type':expense_type,
                'description':f'Travelled Distance: {doc.total_km}km',
                'amount':doc.total_km*(frappe.get_value('Expense Claim Type',expense_type,'ratekm') or 0)
            })
        else:
            frappe.throw('Kindly fill Expense Type in Employee')
        exp_clm.flags.ignore_permissions = True
        exp_clm.save()

        doc.expense_claim = exp_clm.name

@frappe.whitelist()
def create_checkin(start_km=0):
    emp = frappe.get_value("Employee",{'user_id':frappe.session.user},'name')
    if emp:
        if not frappe.get_all('Employee Checkin',{'log_type':'IN','employee':emp,'time':('between',[nowdate(),nowdate()])}):
            doc=frappe.new_doc("Employee Checkin")
            doc.update({
                "start_km":start_km,
                'time':now_datetime(),
                'employee':emp,
                'log_type':'IN'
            })
            doc.insert()
            return doc
        else:
            return 'Checkin already created'

    else:
        frappe.throw(f"Assign your User-ID ({frappe.session.user}) to Employee")

@frappe.whitelist()
def create_checkout(end_km=0, total_km=0):
    emp = frappe.get_value("Employee",{'user_id':frappe.session.user},'name')
    if emp:
        if not frappe.get_all('Employee Checkin',{'log_type':'OUT','employee':emp,'time':('between',[nowdate(),nowdate()])}):
            doc=frappe.new_doc("Employee Checkin")
            doc.update({
                "end_km":float(end_km),
                "total_km":float(total_km),
                "time":now_datetime(),
                'employee':emp,
                'log_type':'OUT'
            })
            doc.insert()
            return doc
        else:
            return 'Checkout Already Created'

    else:
        frappe.throw(f"Assign your User-ID ({frappe.session.user}) to Employee")


@frappe.whitelist()
def validate_checkout():
    emp = frappe.get_value("Employee",{'user_id':frappe.session.user},'name')
    if emp:
        if not frappe.get_all("Employee Checkin", {"time":('between',[nowdate(),nowdate()]),'log_type':'IN', "employee":emp}):
            frappe.throw(f"""Checkin not Found for Date: {now_datetime().strftime("%d-%m-%y")}""")

        return True

    else:
        frappe.throw("Assign this user to Employee")