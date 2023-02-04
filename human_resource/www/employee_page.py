import frappe
def get_context(context):
    context.employees = frappe.db.sql('select * from tabEmployee',as_dict=1)