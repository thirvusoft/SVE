import frappe
from frappe.desk.doctype.note.note import Note

class TSNote(Note):
    def autoname(self):
        pass