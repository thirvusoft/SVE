import frappe
from erpnext.controllers.selling_controller import SellingController
from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_invoice import sales_contribution


class TsSellingController(SellingController):
    def calculate_contribution(self):
        sales_contribution(self)
