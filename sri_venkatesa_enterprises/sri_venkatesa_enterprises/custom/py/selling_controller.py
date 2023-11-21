from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

import frappe
from sri_venkatesa_enterprises.sri_venkatesa_enterprises.custom.py.sales_invoice import sales_contribution
from erpnext.stock.stock_ledger import NegativeStockError

class TsSellingController(SalesInvoice):
    def calculate_contribution(self):
        sales_contribution(self)

class TsSalesOrderSellingController(SalesOrder):
    def calculate_contribution(self):
        sales_contribution(self)

def update():
    si=frappe.get_all("Sales Invoice", filters={"docstatus":1, "updated":1}, pluck="name", order_by="posting_date asc")
    c=0
    print(len(si))
    for i in si:
        c+=1
        print(i, c)
        doc = frappe.get_doc("Sales Invoice", i)
        doc.flags.ignore_validate_update_after_submit = True
        # doc._action="on_cancel"
        # doc.docstatus=2
        # doc.cancel()
        # frappe.db.set_value("Sales Invoice", i, "docstatus", 0, update_modified=False)
        # doc.reload()
        
        # doc._action="validate"
        # doc.run_method("validate")
        # doc.save()
        # doc.reload()
        # doc.docstatus=1
        # doc._action="on_submit"
        # # doc.run_method("on_submit")
        # doc.submit()
        # doc.reload()
        # frappe.db.set_value("Sales Invoice", i, "updated", 1, update_modified=False)
        # frappe.db.commit()
        # continue
        doc.docstatus=2
        if doc.update_stock == 1:
            doc.update_stock_ledger()
        doc.make_gl_entries_on_cancel()
        if doc.update_stock == 1:
            doc.repost_future_sle_and_gle()
        
        doc.docstatus=1
        if doc.update_stock == 1:
            # try:
                doc.update_stock_ledger()
            # except NegativeStockError:
            #     print("NEG")
            #     for j in doc.items:
            #         if j.item_code == "Glycomith 98.9%-25 KG":
            #             frappe.db.set_value("Sales Invoice Item", j.name, "batch_no", "Glycomith 98/9-10/06/23-0002", update_modified=False)
            #             doc.reload()
            #     doc.update_stock_ledger()

        # this sequence because outstanding may get -ve
        doc.make_gl_entries()

        if doc.update_stock == 1:
            doc.repost_future_sle_and_gle()
        frappe.db.set_value("Sales Invoice", i, "updated", 1, update_modified=False)
        frappe.db.commit()

# batch=frappe.get_all("Batch", pluck="name")
# for i in batch:
#     pur=frappe.get_all("Purchase Invoice Item", filters={"docstatus":1, "batch_no":i}, fields=["sum(stock_qty) as qty"], group_by="batch_no")
#     if not pur:
#         pur = frappe.get_all("Purchase Receipt Item", filters={"docstatus":1, "batch_no":i}, fields=["sum(stock_qty) as qty"], group_by="batch_no")
#     if not pur:
#         pur = frappe.get_all("Stock Reconciliation Item", filters={"docstatus":1, "batch_no":i}, fields=["sum(qty) as qty"], group_by="batch_no")
#     si = frappe.get_all("Sales Invoice Item", filters={"docstatus":1, "batch_no":i, "parent":["not in", ["A00177", "A00178", "A00168", "A00172", "A00176", "A00182", "A00187", "A00194"]]}, fields=["sum(stock_qty) as qty"], group_by="batch_no") or [{"qty":0}]
#     bal=frappe.get_value("Batch", i, "batch_qty")
#     if bal != pur[0]["qty"]-si[0]["qty"]:
#         print(i, bal, pur[0]["qty"], si[0]["qty"], pur[0]["qty"]-si[0]["qty"])