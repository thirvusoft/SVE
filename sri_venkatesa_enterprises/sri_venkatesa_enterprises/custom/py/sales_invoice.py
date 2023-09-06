import frappe
from frappe.utils.data import flt
from frappe.contacts.doctype.address.address import address_query
from frappe.model.naming import make_autoname


def sales_contribution(self, event=None):
    self.sales_team = []
    total_contribution = 0
    for spt in self.sales_person_contribution:
        if not spt.get("contribution"):
                frappe.throw(title="Missing Mandatory", msg=f"Row #{spt.idx}: Sales Person contribution % missing")
        total_contribution += spt.contribution or 0
        if total_contribution > 100:
            frappe.throw("Total Sales Person contribution % should be below or equal 100%")
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

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def filter_farm_address(doctype, txt, searchfield, start, page_len, filters):
    from frappe.desk.reportview import get_match_cond

    doctype = "Address"
    link_doctype = filters.pop("link_doctype")
    link_name = []
    if filters.get("party_name"):
        link_name = frappe.get_list("Farm Details", {"customer":filters["party_name"]}, pluck="name")
        del filters["party_name"]
    if not link_name:
        return []

    condition = ""
    meta = frappe.get_meta(doctype)
    for fieldname, value in filters.items():
        if meta.get_field(fieldname) or fieldname in frappe.db.DEFAULT_COLUMNS:
            condition += f" and {fieldname}={frappe.db.escape(value)}"

    searchfields = meta.get_search_fields()

    if searchfield and (meta.get_field(searchfield) or searchfield in frappe.db.DEFAULT_COLUMNS):
        searchfields.append(searchfield)

    search_condition = ""
    for field in searchfields:
        if search_condition == "":
            search_condition += f"`tabAddress`.`{field}` like %(txt)s"
        else:
            search_condition += f" or `tabAddress`.`{field}` like %(txt)s"

    return frappe.db.sql(
        """select
            `tabAddress`.name, `tabAddress`.city, `tabAddress`.country
        from
            `tabAddress`
        join `tabDynamic Link`
            on (`tabDynamic Link`.parent = `tabAddress`.name and `tabDynamic Link`.parenttype = 'Address')
        where
            `tabDynamic Link`.link_doctype = %(link_doctype)s and
            `tabDynamic Link`.link_name in {link_name} and
            ifnull(`tabAddress`.disabled, 0) = 0 and
            ({search_condition})
            {mcond} {condition}
        order by
            case
                when locate(%(_txt)s, `tabAddress`.name) != 0
                then locate(%(_txt)s, `tabAddress`.name)
                else 99999
            end,
            `tabAddress`.idx desc, `tabAddress`.name
        limit %(page_len)s offset %(start)s""".format(
            mcond=get_match_cond(doctype),
            search_condition=search_condition,
            condition=condition or "",
            link_name= f"""("{'","'.join(link_name)}")""",
        ),
        {
            "txt": "%" + txt + "%",
            "_txt": txt.replace("%", ""),
            "start": start,
            "page_len": page_len,
            "link_doctype": link_doctype,
        },
    )


def autoname(doc, event=None):
    if doc.get("branch_series"):
        doc.naming_series = doc.branch_series
        doc.name = make_autoname(doc.branch_series, doc=doc)