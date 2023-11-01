import frappe
def create_expense_claim(doc,event):
    if doc.total_distance > 0 and not doc.expense_claim:
        exp_clm = frappe.new_doc('Expense Claim')
        exp_clm.employee = doc.employee
        exp_clm.expense_approver = frappe.get_value('Employee',doc.employee,'expense_approver')
        company = frappe.get_value('Employee',doc.employee,'company')
        expense_type = frappe.get_value('Employee',doc.employee,'expense_type')
        if expense_type:
            exp_clm.append('expenses',{
                'expense_date':doc.time,
                'expense_type':expense_type,
                'description':f'Travelled Distance: {doc.total_distance}km',
                'amount':doc.total_distance*(frappe.get_value('Expense Claim Type',expense_type,'ratekm') or 0)
            })
        else:
            frappe.throw('Kindly fill Expense Type in Employee')

        exp_clm.save()
        
        doc.expense_claim = exp_clm.name
