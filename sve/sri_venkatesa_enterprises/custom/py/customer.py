import frappe

def maintance_contact_details(doc,actions):
    if doc.doctor_name and doc.doctor_number and (actions == "after_insert" or not doc.is_new()):
        com_add = frappe.get_all("Dynamic Link", {"parenttype": "Contact", "link_doctype": doc.doctype, "link_name": doc.name}, pluck="parent")
        for i in com_add:
            contact = frappe.get_doc("Contact", i)
            if contact.maintenance_type == "Doctor":
                contact.update(
                    {
                        'phone_nos':
                        [{"phone" :doc.doctor_number}], 
                        'first_name':f"{doc.doctor_name} Doctor"
                })
                contact.save(ignore_permissions=True)
        if not frappe.db.exists("Contact", {'maintenance_type': "Doctor"}):
            document_dc = frappe.new_doc("Contact")
            document_dc.first_name = f"{doc.doctor_name} Doctor"
            document_dc.maintenance_type = "Doctor"
            document_dc.append('phone_nos', 
                            dict(
                                    phone = doc.doctor_number,
                                    is_primary_mobile_no = 1
                                    ))
            document_dc.append('links', 
                            dict(
                                    link_doctype = doc.doctype,
                                    link_name = doc.name
                                    ))
            document_dc.save(ignore_permissions=True)

    if doc.dealer_name and doc.dealer_contact_no and (actions == "after_insert" or not doc.is_new()):
        com_add = frappe.get_all("Dynamic Link", {"parenttype": "Contact", "link_doctype": doc.doctype, "link_name": doc.name}, pluck="parent")
        for i in com_add:
            contact = frappe.get_doc("Contact", i)
            if contact.maintenance_type == "Dealer":
                contact.update(
                    {
                        'phone_nos':
                        [{"phone" :doc.dealer_contact_no}], 
                        'first_name':f"{doc.dealer_name} Dealer"
                })
                contact.save(ignore_permissions=True)
        if not frappe.db.exists("Contact", {'maintenance_type': "Dealer"}):
            document_dc = frappe.new_doc("Contact")
            document_dc.first_name = f"{doc.dealer_name} Dealer"
            document_dc.maintenance_type = "Dealer"
            document_dc.append('phone_nos', 
                            dict(
                                    phone = doc.dealer_contact_no,
                                    is_primary_mobile_no = 1
                                    ))
            document_dc.append('links', 
                            dict(
                                    link_doctype = doc.doctype,
                                    link_name = doc.name
                                    ))
            document_dc.save(ignore_permissions=True)
    if doc.supervisor_name and doc.supervisor_number and (actions == "after_insert" or not doc.is_new()):
        com_add = frappe.get_all("Dynamic Link", {"parenttype": "Contact", "link_doctype": doc.doctype, "link_name": doc.name}, pluck="parent")
        for i in com_add:
            contact = frappe.get_doc("Contact", i)
            if contact.maintenance_type == "Supervisor":
                contact.update(
                    {
                        'phone_nos':
                        [{"phone" :doc.supervisor_number}], 
                        'first_name':f"{doc.supervisor_name} Supervisor"
                })
                contact.save(ignore_permissions=True)
        if not frappe.db.exists("Contact", {'maintenance_type': "Supervisor"}):
            document_dc = frappe.new_doc("Contact")
            document_dc.first_name = f"{doc.supervisor_name} Supervisor"
            document_dc.maintenance_type = "Supervisor"
            document_dc.append('phone_nos', 
                            dict(
                                    phone = doc.supervisor_number,
                                    is_primary_mobile_no = 1
                                    ))
            document_dc.append('links', 
                            dict(
                                    link_doctype = doc.doctype,
                                    link_name = doc.name
                                    ))
            document_dc.save(ignore_permissions=True)
