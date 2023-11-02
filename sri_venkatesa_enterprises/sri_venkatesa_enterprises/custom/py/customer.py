import frappe
from frappe import _
from frappe.utils.data import cint, cstr
from erpnext.selling.doctype.customer.customer import Customer

def maintance_contact_details(doc,actions):
  
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
        if not frappe.db.exists("Contact", {'maintenance_type': "Dealer", "name" : ['in',com_add]}):
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
        if not frappe.db.exists("Contact", {'maintenance_type': "Supervisor", "name" : ['in',com_add]}):
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

def set_exisiting_farm(doc,actions):
    if doc.name  and (actions == "after_insert" or not doc.is_new()):
        if doc.lead_name:
            farm_details = frappe.get_value("Farm Details", {"lead": doc.lead_name},"name")
            if farm_details:
                farm = frappe.get_doc("Farm Details", farm_details)
                if farm.lead == doc.lead_name:
                    farm.update(
                        {
                            'customer':doc.name
                    })
                    farm.save(ignore_permissions=True)


@frappe.whitelist()
def get_farm_list(ref_doctype, ref_name):
    if(not ref_doctype or not ref_name):
        return
    field = frappe.scrub(ref_doctype)
    farm_list = frappe.get_all("Farm Details", filters={field:ref_name}, fields=["*"])
    for i in farm_list:
        i['compatible_breed'] = ", ".join(frappe.get_all("Compatible Breed Table", filters={"parent":i['name']}, pluck="compatible_breed"))
        i["display"] = ""
        if(i["farm_name"]):
            i["display"] += f"""
            <p>Farm: {i["farm_name"] or ""}</p>
                """
        if(i["farm_location"]):
            i["display"] += f"""
            <p>Loc: {i["farm_location"] or ""}</p>
                """
        if(i["ton_of_feed"]):
            i["display"] += f"""
            <p>Ton of Feed: {i["ton_of_feed"] or ""}</p>
                """
        if(i["chick_capacity__laying"]):
            i["display"] += f"""
            <p>Laying Capacity: {i["chick_capacity__laying"] or ""}</p>
                """
        if(i["compatible_breed"]):
            i["display"] += f"""
             <p>Compatible Breeds: {i["compatible_breed"] or ""}</p>
                """
    return farm_list

def create_farm(self, event=None):
    if self.flags.is_new_doc and self.get("batch_size"):
        doc = frappe.new_doc('Farm Details')
        doc.update({
            "customer": self.name,
            "chick_capacity__laying": self.get("batch_size"),
            "farm_name": (self.get('customer_name') or '') + ' Farm'
        })
        if frappe.db.get_value("Farm Details", doc.get("farm_name")) and not frappe.flags.in_import:
            count = frappe.db.sql(
                """select ifnull(MAX(CAST(SUBSTRING_INDEX(name, ' ', -1) AS UNSIGNED)), 0) from `tabFarm Details`
                    where name like %s""",
                "%{0} - %".format(self.customer_name),
                as_list=1,
            )[0][0]
            count = cint(count) + 1

            doc.update({
                "__newname": "{0} - {1}".format(self.customer_name, cstr(count))
            })

        doc.insert()


class TSCustomer(Customer):
    def create_primary_contact(self):
        if not self.customer_primary_contact and not self.lead_name:
            if self.mobile_no or self.email_id:
                contact = make_contact(self)
                self.db_set("customer_primary_contact", contact.name)
                self.db_set("mobile_no", self.mobile_no)
                self.db_set("email_id", self.email_id)

    def create_primary_address(self):
        from frappe.contacts.doctype.address.address import get_address_display

        if self.flags.is_new_doc and self.get("address_line1"):
            address = make_address(self)
            address_display = get_address_display(address.name)

            self.db_set("customer_primary_address", address.name)
            self.db_set("primary_address", address_display)

def make_contact(args, is_primary_contact=1):
    contact = frappe.get_doc(
        {
            "doctype": "Contact",
            "first_name": args.get("name"),
            "is_primary_contact": is_primary_contact,
            "designation": args.get("designation"),
            "links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
        }
    )
    if args.get("email_id"):
        contact.add_email(args.get("email_id"), is_primary=True)
    if args.get("mobile_no"):
        contact.add_phone(args.get("mobile_no"), is_primary_mobile_no=True)
    contact.insert()

    return contact

def make_address(args, is_primary_address=1):
    reqd_fields = []
    for field in ["city", "country"]:
        if not args.get(field):
            reqd_fields.append("<li>" + field.title() + "</li>")

    if reqd_fields:
        msg = _("Following fields are mandatory to create address:")
        frappe.throw(
            "{0} <br><br> <ul>{1}</ul>".format(msg, "\n".join(reqd_fields)),
            title=_("Missing Values Required"),
        )
    frappe.errprint(args.get("gstin") or "None")
    address = frappe.get_doc(
        {
            "doctype": "Address",
            "address_title": args.get("name"),
            "address_line1": args.get("address_line1"),
            "address_line2": args.get("address_line2"),
            "city": args.get("city"),
            "custom_district": args.get("district"),
            "state": args.get("state"),
            "pincode": args.get("pincode"),
            "custom_aadhar_no": args.get("aadhar_no"),
            "country": args.get("country") or "India",
            "gstin": args.get("gstin"),
            "links": [{"link_doctype": args.get("doctype"), "link_name": args.get("name")}],
            "gst_category": "Registered Regular" if args.get("gstin") else "Unregistered",
        }
    ).insert()

    return address