from erpnext.controllers.taxes_and_totals import get_itemised_tax
import frappe
from frappe.utils.data import cint

def get_invoice_item_and_tax_details(voucher_type, voucher_no):
    doc = frappe.get_doc(voucher_type, voucher_no)
    itemised_tax = get_itemised_tax(doc.taxes)
    items = doc.items
    instate = False
    outstate = False
    total_cgst, total_sgst, total_igst = 0, 0, 0
    tax_details = {}
    for row in items:
        if row.item_code in itemised_tax:
            cgst, sgst, igst = 0, 0, 0
            for tax in itemised_tax.get(row.item_code):
                
                if 'cgst' in (tax or '').lower() and (itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0):
                    instate = True
                    row.cgst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.cgst_percent = f"{cint(row.cgst) if cint(row.cgst)==row.cgst else row.cgst}%"
                    cgst += row.amount * row.cgst / 100

                elif 'sgst' in (tax or '').lower() and (itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0):
                    instate = True
                    row.sgst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.sgst_percent = f"{cint(row.sgst) if cint(row.sgst)==row.sgst else row.sgst}%"
                    sgst += row.amount * row.sgst / 100

                elif 'igst' in (tax or '').lower() and (itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0):
                    outstate = True
                    row.igst = itemised_tax.get(row.item_code).get(tax).get('tax_rate') or 0
                    row.igst_percent = f"{cint(row.igst) if cint(row.igst)==row.igst else row.igst}%"
                    igst += row.amount * row.igst / 100
                
            tax_percent = (row.get('cgst') or 0) + (row.get('sgst') or 0) + (row.get('igst') or 0)
            if tax_percent not in tax_details:
                tax_details[tax_percent] = {
                    'tax_percentage': f"{cint(tax_percent) if cint(tax_percent)==tax_percent else tax_percent}%",
                    'taxable_amount': row.net_amount or 0,
                    'cgst': cgst,
                    'sgst': sgst,
                    'igst': igst,
                    'total_tax_amount': (cgst or 0) + (sgst or 0) + (igst or 0)
                }
            else:
                tax_details[tax_percent]['taxable_amount'] += row.net_amount or 0
                tax_details[tax_percent]['cgst'] += cgst
                tax_details[tax_percent]['sgst'] += sgst
                tax_details[tax_percent]['igst'] += igst
                tax_details[tax_percent]['total_tax_amount'] += (cgst or 0) + (sgst or 0) + (igst or 0)

            total_cgst += cgst
            total_sgst += sgst
            total_igst += igst

    return {
        "items": items,
        "instate": instate,
        "outstate": outstate,
        "tax_details": list(tax_details.values()) + [{
            'tax_percentage': 'Totals',
            'taxable_amount': doc.net_total,
            'cgst': total_cgst,
            'sgst': total_sgst,
            'igst': total_igst,
            'total_tax_amount': (total_cgst or 0) + (total_sgst or 0) + (total_igst or 0)
        }],
        "cgst": total_cgst,
        "sgst": total_sgst,
        "igst": total_igst,
    }
