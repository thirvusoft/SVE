import frappe
from frappe.utils.data import flt

def sales_contribution(self, event=None):
    self.sales_team = []
    for spt in self.sales_person_contribution:
        for item in self.items:

            self.append('sales_team', 
                dict(
                        sales_person = spt.sales_person,
                        item = item.item_code,
                        allocated_percentage = spt.contribution,
                        commission_rate = item.sales_person_commission_rate,
                        allocated_amount = flt(item.amount * spt.contribution / 100.0),
                        incentives = flt(item.amount * spt.contribution / 100.0) * flt(item.sales_person_commission_rate) / 100.0,
                        ))

# def calculate_contribution(self):
# 	if not self.meta.get_field("sales_team"):
# 		return

# 	total = 0.0
# 	sales_team = self.get("sales_team")
# 	for sales_person in sales_team:
# 		self.round_floats_in(sales_person)
# 		sales_person.allocated_amount = flt(
# 			self.amount_eligible_for_commission * sales_person.allocated_percentage / 100.0,
# 			self.precision("allocated_amount", sales_person),
# 		)

# 		if sales_person.commission_rate:
# 			sales_person.incentives = flt(
# 				sales_person.allocated_amount * flt(sales_person.commission_rate) / 100.0,
# 				self.precision("incentives", sales_person),
# 			)

# 		total += sales_person.allocated_percentage

# 	if sales_team and total != 100.0:
# 		throw(_("Total allocated percentage for sales team should be 100"))