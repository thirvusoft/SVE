import frappe
from frappe.utils import get_datetime, getdate, date_diff

def validate_return(doc,actions):
    if doc.is_return == 1:
        so = frappe.get_doc("Delivery Note",doc.return_against)
        start_date = so.posting_date
        end_date = doc.posting_date
        date1 = get_datetime(start_date)
        date2 = get_datetime(end_date)
        days_difference = date_diff(date2, date1)
        print(days_difference)
        for i in doc.items:
            so_items = frappe.get_doc("Item",i.item_code)
            if so_items.delivery_date:
                if days_difference > int(so_items.delivery_date):
                    frappe.throw(f"{i.item_code} Return date is greater than posting date")