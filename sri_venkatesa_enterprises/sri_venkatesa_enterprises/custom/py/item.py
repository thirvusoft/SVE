import frappe
import erpnext
import json
from frappe.utils import (
	cint,
	cstr,
	flt,
	formatdate,
	get_link_to_form,
	getdate,
	now_datetime,
	nowtime,
	strip,
	strip_html,
)

from frappe.utils import strip, now,get_datetime, nowtime
from frappe import _

def update_price(doc, actions=None):
    if doc.is_new():
        return
    if doc.selling_rate:
        ip = frappe.get_all('Item Price', {'price_list':"Standard Selling", 'item_code':doc.name, 'valid_upto':["is","not set"]}, 'name')
        if(ip):
            exists_doc = frappe.get_doc('Item Price', ip[0].name)
            if exists_doc.price_list_rate != doc.selling_rate:
                exists_doc.valid_upto = now()
                exists_doc.save()
                item_price = frappe.get_doc(
                    {
                            "doctype": "Item Price",
                            "price_list": "Standard Selling",
                            "item_code": doc.name,
                            "uom": doc.stock_uom,
                            "currency": erpnext.get_default_currency(),
                            "price_list_rate": doc.selling_rate or 0,
                        }
                    )
                item_price.flags.ignore_links = True
                item_price.save()
        elif(doc.selling_rate):
            item_price = frappe.get_doc(
                {
                            "doctype": "Item Price",
                            "price_list": "Standard Selling",
                            "item_code": doc.name,
                            "uom": doc.stock_uom,
                            "currency": erpnext.get_default_currency(),
                            "price_list_rate": doc.selling_rate or 0,
                        }
                    )
            item_price.flags.ignore_links = True
            item_price.save()
    if doc.buying_rate:
        ip = frappe.get_all('Item Price', {'price_list':"Standard Buying", 'item_code':doc.name, 'valid_upto':["is","not set"]}, 'name')
        if(ip):
            exists_doc = frappe.get_doc('Item Price', ip[0].name)
            if exists_doc.price_list_rate != doc.buying_rate:
                exists_doc.valid_upto = now()
                exists_doc.save()
                item_price_buy = frappe.get_doc(
                    {
                            "doctype": "Item Price",
                            "price_list": "Standard Buying",
                            "item_code": doc.name,
                            "uom": doc.stock_uom,
                            "currency": erpnext.get_default_currency(),
                            "price_list_rate": doc.buying_rate or 0,
                        }
                    )
                item_price_buy.flags.ignore_links = True
                item_price_buy.save()
        elif(doc.buying_rate):
            item_price_buy = frappe.get_doc(
                {
                            "doctype": "Item Price",
                            "price_list": "Standard Buying",
                            "item_code": doc.name,
                            "uom": doc.stock_uom,
                            "currency": erpnext.get_default_currency(),
                            "price_list_rate": doc.buying_rate or 0,
                        }
                    )
            item_price_buy.flags.ignore_links = True
            item_price_buy.save()
        


def validate(doc, event=None):
    update_price(doc)
    remove_tax_for_nil_rated(doc)

def remove_tax_for_nil_rated(doc):
    if doc.is_non_gst or doc.is_nil_exempt and doc.taxes:
        doc.taxes = []