import frappe

import json
import os
import frappe
from frappe.utils import get_url
from pyqrcode import create as qrcreate


def qrcode_as_png(doc, content):
    """Save temporary Qrcode to server."""
    png_file_name = "{}.png".format(doc+'_payment_url')
    old_file = frappe.db.get_value('File', {"attached_to_field":'custom_qr_file_url', 'attached_to_name':doc}, 'name')
    if(old_file):
        frappe.delete_doc('File', old_file)
    _file = frappe.get_doc(
        {
            "doctype": "File",
            "file_name": png_file_name,
            "attached_to_doctype": "Payment Entry",
            "attached_to_name": doc,
            "content": png_file_name,
            "attached_to_field":'custom_qr_file_url',
        }
    )
    _file.save()
    file_url = get_url(_file.file_url)
    file_path = os.path.join(frappe.get_site_path("public", "files"), _file.file_name)
    url = qrcreate(content)
    with open(file_path, "wb") as png_file:
        url.png(png_file, scale=4)
    return _file.file_url

@frappe.whitelist()
def set_qr_image(doc):
    doc=json.loads(doc)
    if doc["docstatus"] ==1:
        upi_id = frappe.db.get_value('Branch', doc["branch"], 'custom_upi_id')
        if upi_id:
            company=doc["company"]
            paid_amount=doc["paid_amount"]
            name=doc["name"]
            content = f"upi://pay?pa={upi_id}&pn={company}&am={paid_amount}&cu=INR&tn={name}"
            file_url = qrcode_as_png(name, content)
            payment_doc=frappe.get_doc("Payment Entry", doc["name"])
            if payment_doc:
                payment_doc.custom_qr_file_url= file_url
                payment_doc.custom_upi_id = upi_id
                payment_doc.save()
                return True
