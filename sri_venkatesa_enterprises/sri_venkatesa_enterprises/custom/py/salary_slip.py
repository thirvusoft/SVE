import frappe
import sri_venkatesa_enterprises as sve
from hrms.payroll.doctype.salary_slip.salary_slip import SalarySlip

class TSSalarySlip(SalarySlip):
    def eval_condition_and_formula(self, struct_row, data):
        data.update({"sum":sum, "frappe":frappe, "sve":sve})
        return super(TSSalarySlip, self).eval_condition_and_formula(struct_row, data)
    


# sum([sve.get_travel_expense(i["vehicle_used"], i["total_km"]) for i in frappe.get_all("Employee Checkin", filters={"employee":employee, "time":["between", (start_date, end_date)]}, fields=["total_km", "vehicle_used"])])