# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt
import datetime

import frappe
from frappe.model.document import Document
from frappe import utils


class Attendance(Document):
    def before_save(self):
        self.calculate_work_late_hours()

    def on_submit(self):
        self.get_status()

    def calculate_work_late_hours(self):
        settings = get_attendance_settings()
        start_time = datetime.datetime.strptime(settings.start_time, '%H:%M:%S')
        end_time = datetime.datetime.strptime(settings.end_time, '%H:%M:%S')
        check_in = datetime.datetime.strptime(self.check_in, '%H:%M:%S')
        check_out = datetime.datetime.strptime(self.check_out, '%H:%M:%S')
        start_time_plus_grace_period = start_time + datetime.timedelta(minutes=float(settings.late_entry_grace_period))
        end_time_minus_grace_period = end_time - datetime.timedelta(minutes=float(settings.early_exit_grace_period))
        if check_in >= check_out:
            frappe.throw('check out time must be bigger than check in time')
        if check_in <= start_time_plus_grace_period:
            check_in = start_time
        if end_time_minus_grace_period <= check_out:
            check_out = end_time
        work_hours = frappe.utils.time_diff_in_hours(check_out, check_in)
        self.work_hours = work_hours
        late_hours = frappe.utils.time_diff_in_hours(end_time, start_time) - work_hours
        self.late_hours = late_hours

    def get_status(self):
        settings = get_attendance_settings()
        working_hours_threshold_for_absent = settings.working_hours_threshold_for_absent
        if self.work_hours < working_hours_threshold_for_absent:
            self.status = 'Absent'


def get_attendance_settings():
    return frappe.get_single('Attendance Settings').as_dict()

# def calculate_work__hours( check_in, check_out):
#     if employee and check_in and check_out:
#         settings = get_attendance_settings()
#         total_work_hours = frappe.utils.time_diff_in_hours(check_out, check_in)
#         total_company_work_hours = frappe.utils.time_diff_in_hours(settings.end_time, settings.start_time)
#         if total_work_hours >= total_company_work_hours:
#             return total_company_work_hours
#         else:
#             check_in_plus_grace_period = datetime.datetime.strptime(check_in, '%H:%M:%S') + datetime.timedelta(
#                 minutes=float(settings.late_entry_grace_period))
#             check_out_plus_grace_period = datetime.datetime.strptime(check_out, '%H:%M:%S') + datetime.timedelta(
#                 minutes=float(settings.early_exit_grace_period))
#             return frappe.utils.time_diff_in_hours(str(check_out_plus_grace_period),
# #                                                    str(check_in_plus_grace_period))
#     else:
#         return
