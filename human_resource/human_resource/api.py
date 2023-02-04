import frappe
import datetime


@frappe.whitelist()
def create_attendance(attendance_date, check_in, check_out, ):
    api_key = str(frappe.get_request_header("Authorization")).split(':')[0].split(' ')[-1]
    user = frappe.db.sql(f"""select * from tabUser where api_key = '{api_key}' """, as_dict=1)[0].name
    employee = frappe.db.sql(f""" select name from `tabEmployee` where user = '{user}' """, as_dict=1)[0].name
    doc = frappe.new_doc('Attendance')
    doc.employee = employee
    doc.attendance_date = datetime.datetime.strptime(str(attendance_date).strip(), '%d-%m-%Y')
    doc.check_in = check_in
    doc.check_out = check_out
    doc.save()
    doc.submit()


    return doc.as_dict()
