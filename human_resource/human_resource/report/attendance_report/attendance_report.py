# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = [
        {'fieldname': 'employee', 'label': _('Employee'), 'fieldtype': 'Link', 'options': 'Employee'},
        {'fieldname': 'employee_name', 'label': _('Employee Name'), 'fieldtype': 'data'},
        {'fieldname': 'attendance_date', 'label': _('Attendance Date'), 'fieldtype': 'date'},
        {'fieldname': 'status', 'label': _('Status'), 'fieldtype': 'select', 'options': ['Present', 'Absent']},
        {'fieldname': 'check_in', 'label': _('Check In'), 'fieldtype': 'time'},
        {'fieldname': 'check_out', 'label': _('Check Out'), 'fieldtype': 'time'},
        {'fieldname': 'work_hours', 'label': _('Work Hours'), 'fieldtype': 'float'},
        {'fieldname': 'late_hours', 'label': _('Late Hours'), 'fieldtype': 'float'},
    ]
    # data = frappe.db.sql(
    #     """select employee , employee_name , attendance_date ,department , status, check_in,check_out, work_hours ,
    #     late_hours from `tabAttendance` """,
    #     as_dict=1, filters=filters)
    data = frappe.db.get_all('Attendance',
                             ['employee', 'employee_name', 'attendance_date', 'department', 'status', 'check_in',
                              'check_out', 'work_hours', 'late_hours'], filters=filters)

    for d in data:
        d.work_hours = round(d.work_hours, 2)
        d.late_hours = round(d.late_hours, 2)

    return columns, data
