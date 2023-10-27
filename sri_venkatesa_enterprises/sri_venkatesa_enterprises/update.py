import frappe

def update_sve_route_user_permission():
	user = frappe.get_all("User", pluck="name")
	for i in user:
		if frappe.db.exists("User Permission", {"user":i, "allow":"Territory"}):
			perms = frappe.get_all("User Permission", filters={"user":i, "allow":"Territory"}, pluck="for_value")
			for j in perms:
				if j != "All Territories":
					parent = frappe.get_value("Territory", j, "parent_territory")
					parent_doc=frappe.get_doc("Territory", parent)
					if not frappe.has_permission(doctype="Territory", user=i, doc=parent_doc):
						user_perm = frappe.new_doc("User Permission")
						user_perm.update({
							"user":i,
							"allow":"Territory", 
							"for_value":parent,
							"apply_to_all_doctypes":1,
							"hide_descendants":1
						})
						user_perm.save()
						perms.append(parent)