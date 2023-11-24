# Copyright (c) 2023, Thirvusoft and contributors
# For license information, please see license.txt

import frappe
import calendar
from datetime import datetime, timedelta
from frappe.query_builder.functions import Count, Extract, Sum
from frappe.utils import cint, cstr, getdate

def execute(filters=None):
	columns, data = get_columns(), get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"fieldname":"category",
			"label":"Category",
			"fieldtype":"Data",
			"width":200
		},
		{
			"fieldname":"payment_amount",
			"label":"Payment Amount",
			"fieldtype":"Currency",
			"width":150
		},
		{
			"fieldname":"incentive_percentage",
			"label":"Incentive %",
			"fieldtype":"Data",
			"width":100
		},
		{
			"fieldname":"incentive_amount",
			"label":"Incentive Amount",
			"fieldtype":"Currency",
			"width":150
		},
	]
	return columns
def get_data(filters):
	data =[]
	quarterly = ["3","6","9","12"]
	half_yearly = ["6","12"]
	total_eligible_amount = 0
	settings = frappe.get_single("Incentive Settings")
	to_month = from_month = filters.get("month")
	year = filters.get("year")
	month_list = monthly("Monthly",year,from_month,to_month,filters,settings)
	data = data + month_list
	if month_list[0]["eligible"] == "1":
		for i in month_list:
			total_eligible_amount = total_eligible_amount + i["incentive_amount"]
	if filters.get("month") in quarterly:
		month_list = monthly("Quarterly",year,int(from_month)-2,to_month,filters,settings)
		data = data + month_list
		if month_list[0]["eligible"] == "1":
			total_eligible_amount = total_eligible_amount + month_list[0]["incentive_amount"]

	if filters.get("month") in half_yearly:
		month_list = monthly("Half yearly",year,int(from_month)-5,to_month,filters,settings)
		data = data + month_list
		if month_list[0]["eligible"] == "1":
			total_eligible_amount = total_eligible_amount + month_list[0]["incentive_amount"]
		
	if filters.get("month") == "12":
		month_list = monthly("Yearly",year,int(from_month)-11,to_month,filters,settings)
		data = data + month_list
		if month_list[0]["eligible"] == "1":
			total_eligible_amount = total_eligible_amount + month_list[0]["incentive_amount"]
	data.append({"category":"Total Eligible Amount","incentive_amount":total_eligible_amount})
	return data
	
def monthly(type,year,from_month,to_month,filters,settings):
	monthly_nodue_days=settings.no_due_days
	last_day = calendar.monthrange(int(year), int(to_month))
	from_date = f"{year}-{int(from_month):02d}-01"
	to_date = f"{year}-{int(to_month):02d}-{last_day[1]}"
	to_date_1 = datetime.strptime(to_date, '%Y-%m-%d')
	salesperson=filters.get("sales_person")
	result_date = to_date_1 - timedelta(days=monthly_nodue_days)
	payment_sales=frappe.db.sql(f'''
		SELECT 
			pr.allocated_amount as payment_amount, 
			(DATEDIFF(pe.posting_date, si.posting_date) + 1) as daydiff
		FROM `tabPayment Entry` as pe 
		INNER JOIN `tabPayment Entry Reference` as pr
			ON pr.parent = pe.name
			and pr.reference_doctype = 'Sales Invoice'
		INNER JOIN `tabSales Invoice` as si
			ON si.name = pr.reference_name
		INNER JOIN `tabSales Team` as st
			ON st.parent = si.name
			and st.sales_person = '{salesperson}'
		WHERE 
			pe.posting_date between '{from_date}' AND '{to_date}' and
			pe.docstatus = 1 and
			si.outstanding_amount = 0 and
			si.docstatus = 1
		''', as_dict=1)
	sales_payment=frappe.db.sql(f'''
		SELECT 
			(si.grand_total - pr.allocated_amount) as outstanding,si.name,si.posting_date,pr.parent
		FROM `tabSales Invoice` as si
		INNER JOIN `tabSales Team` as st
			ON st.parent = si.name
			and st.sales_person = '{salesperson}'
		INNER JOIN `tabPayment Entry Reference` as pr
			ON pr.reference_name = si.name
			and pr.reference_doctype = 'Sales Invoice'
		INNER JOIN `tabPayment Entry` as pe
			ON pe.name = pr.parent
			and pe.posting_date > DATE('{to_date}')
			and pe.docstatus = 1
		WHERE 
			si.posting_date < DATE('{result_date}') and
			si.docstatus = 1 and
			si.status NOT IN ("Return", "Credit Note Issued")

		''', as_dict=1)
	non_payment = frappe.db.get_list("Sales Invoice", filters=[["docstatus","=", 1],                             
					["status", "not in", ["Paid", "Return", "Credit Note Issued"]],
					["Sales Team", "sales_person", "=", filters.get("sales_person")],
					["posting_date", "<", result_date]],
					fields=["outstanding_amount"])

	sales_invoice = sales_payment+non_payment
	data = {}
	eligible = 0
	monthly_percentage=[]
	if type == "Monthly":
		for row in payment_sales:
			if row.daydiff <= monthly_nodue_days:
				incentive_details=frappe.db.get_all("Monthly Incentive Percentage", {"below_days": [">=", row.daydiff]}, ["incentive_percentage", "below_days"], order_by="below_days")
				if not incentive_details:
					continue
				incentive_details = incentive_details[0]
				row.incentive_percentage = incentive_details.incentive_percentage or 0
				row.category = f"Below {int(incentive_details.below_days or 0)} days"
				row.incentive_amount = (row.payment_amount or 0) * row.incentive_percentage / 100
				monthly_percentage.append(incentive_details.below_days)
			else:
				eligible = eligible + 1
				row.category = f"Above {int(monthly_nodue_days)} days"
				row.incentive_amount = 0
				row.incentive_percentage = 0
	
			if row.category not in data:
				data[row.category] = row
			else:
				data[row.category]['incentive_amount'] += (row.incentive_amount or 0)
				data[row.category]['payment_amount'] += (row.payment_amount or 0)
		reamining_days=frappe.db.get_all("Monthly Incentive Percentage", {"below_days": ["not in",monthly_percentage ]}, ["incentive_percentage", "below_days"])
		for days in reamining_days:
			day={}
			day["category"]= f"Below {int(days.below_days or 0)} days"
			day["incentive_percentage"] = days.incentive_percentage or 0
			day["incentive_amount"] = 0
			data["category"] = day
		return [{'is_month_row':1, 'eligible':'1' if not sales_invoice else '0' ,'category': f"{type}{' - Eligible' if not sales_invoice else ' - Not Eligible'}","incentive_amount":0,"payment_amount":0}] + (list(sorted(data.values(),key=lambda row: row["category"])))
	elif type == "Quarterly":
		return [{'is_row':1, 'eligible':'1' if not sales_invoice else '0', 'category': f"{type}{' - Eligible' if not sales_invoice else ' - Not Eligible'}","incentive_amount":settings.fixed_incentive_amount_quarterly,"payment_amount":0	}]
	elif type == "Half yearly":
		return [{'is_row':1, 'eligible':'1' if not sales_invoice else '0', 'category': f"{type}{' - Eligible' if not sales_invoice else ' - Not Eligible'}","incentive_amount":settings.fixed_incentive_amount_half_yearly,"payment_amount":0	}]
	elif type == "Yearly":
		return [{'is_row':1, 'eligible':'1' if not sales_invoice else '0', 'category': f"{type}{' - Eligible' if not sales_invoice else ' - Not Eligible'}","incentive_amount":settings.fixed_incentive_amount__yearly,"payment_amount":0	}]

@frappe.whitelist()
def get_invoiced_years() -> str:
	"""Returns all the years for which invoiced records exist"""
	invoiced = frappe.qb.DocType("Sales Invoice")
	year_list = (
		frappe.qb.from_(invoiced)
		.select(Extract("year", invoiced.posting_date).as_("year"))
		.distinct()
	).run(as_dict=True)

	if year_list:
		year_list.sort(key=lambda d: d.year, reverse=True)
	else:
		year_list = [getdate().year]

	return "\n".join(cstr(entry.year) for entry in year_list)