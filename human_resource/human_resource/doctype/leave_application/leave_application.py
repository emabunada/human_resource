# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from _datetime import datetime
from frappe.utils import date_diff


# dob = datetime.strptime(self.employee_date_of_birth, '%Y-%m-%d').date() """ 1- When save Leave Application  Get
# Value Total Leave Days "diff between from date and to date value in leave application" and Leave Balance Before
# Application  "value from Leave Allocation for same employee"
# 2- Add Validate when create or save Leave Application For Employee if Total Leave Days more than Total Leave Days
# 3- when submit Leave Application  update Value ON  Leave Allocation Total Leave Days
# """
class LeaveApplication(Document):
    def before_save(self):
        self.get_total_leave_days()
        self.get_allocation_balance()
        self.validate_leave_days()
        self.update_allocation_balance()

    def get_total_leave_days(self):
        to_date = datetime.strptime(self.to_date, '%Y-%m-%d').date()
        from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
        date_dif = date_diff(self.to_date, self.from_date)
        self.total_leave_days = date_dif

    def get_allocation_balance(self):
        allocations = frappe.db.get_list('Leave Allocation',
                                         filters={'employee': self.employee, 'leave_type': self.leave_type})

        if len(allocations) > 0:
            allocation_name = allocations[0].name
            allocation_days = frappe.get_value('Leave Allocation', allocation_name, ['total_leaves_allocated'])
            self.leave_balance = allocation_days
        else:
            frappe.throw(f"لايوجد اجازات من هذا النوع للموظف  {self.employee_name}")
            # frappe.db.get_value("[doctype]", "[name]", "fieldname")

    def validate_leave_days(self):
        if int(self.leave_balance) < int(self.total_leave_days):
            frappe.msgprint(f"{self.leave_balance} {self.total_leave_days}")
            frappe.throw("خطا عدد الايام المدخل اكبر من المسموح به ")

    def update_allocation_balance(self):
        allocation_name = frappe.db.get_list('Leave Allocation',
                                             filters={'employee': self.employee, 'leave_type': self.leave_type})[0].name

        allocation = frappe.get_doc("Leave Allocation", allocation_name)
        allocation.total_leaves_allocated = self.leave_balance - self.total_leave_days
        allocation.save()
