# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt
import frappe
# import frappe
from frappe.model.document import Document
from _datetime import datetime
from frappe.utils import date_diff


# dob = datetime.strptime(self.employee_date_of_birth, '%Y-%m-%d').date() """ 1- When save Leave Application  Get


class LeaveApplication(Document):
    def before_save(self):
        self.validate_if_from_date_after_to_date()
        self.get_total_leave_days()
        self.get_allocation_balance()
        self.validate_leave_days()
        self.validate_max_continuous_leave_days()
        self.validate_leave_date_if_allow_after()

    def on_submit(self):
        self.update_allocation_balance_on_submit()

    def on_cancel(self):
        self.update_allocation_balance_on_cancel()

    def get_total_leave_days(self):
        date_dif = date_diff(self.to_date, self.from_date) + 1

        self.total_leave_days = date_dif

    def get_current_allocation_name(self):
        leave_allocations = frappe.db.sql(
            """ select name from `tabLeave Allocation` where employee_name = %s
        and leave_type = %s and from_date <= %s and to_date >= %s
        """, (self.employee_name, self.leave_type, self.from_date, self.to_date), as_dict=1)
        if leave_allocations:
            return leave_allocations[0]

    def get_allocation_balance(self):
        allocation_name = self.get_current_allocation_name()
        allocation_doc = frappe.get_doc('Leave Allocation', allocation_name)
        if allocation_doc:
            allocation_days = allocation_doc.total_leaves_allocated
            self.leave_balance_before_application = allocation_days

        else:
            frappe.throw(f"لايوجد اجازات من هذا النوع للموظف  {self.employee_name}")
            # frappe.db.get_value("[doctype]", "[name]", "fieldname")

    def validate_leave_days(self):
        if float(self.leave_balance_before_application) < float(self.total_leave_days):
            frappe.throw("خطا عدد الايام المدخل اكبر من المسموح به ")

    def update_allocation_balance_on_submit(self):
        allocation_name = self.get_current_allocation_name()

        allocation = frappe.get_doc("Leave Allocation", allocation_name)
        allocation.total_leaves_allocated = float(self.leave_balance_before_application) - float(self.total_leave_days)
        allocation.save()

    def update_allocation_balance_on_cancel(self):
        allocation_name = self.get_current_allocation_name()
        allocation = frappe.get_doc("Leave Allocation", allocation_name)
        allocation.total_leaves_allocated = float(allocation.total_leaves_allocated) + float(self.total_leave_days)
        allocation.save()
        # 1- When Cancel  Leave Application  update Value  Leave Balance Before Application   from Leave Allocation
        self.leave_balance_before_application = allocation.total_leaves_allocated

    # 2- Add Validate when create or save Leave Application  if from date value  after to date value
    # 5- add field “checkbox” Allow Negative Balance in Leave Type

    def validate_if_from_date_after_to_date(self):
        allow_negative_balance = frappe.get_doc("Leave Type", self.leave_type).allow_negative_balance
        date_dif = date_diff(self.to_date, self.from_date)
        if date_dif < 0 and not allow_negative_balance:
            frappe.throw(f'خطا, تاريخ نهاية الاجازة يجب ان يكون بعد تاريخ البداية في الاجازة {self.leave_type}')

    # 4- Add field “Max Continuous Days Allowed”  in Leave Type and add validate on leave application If Total leave days more than Max Continuous Days Allowed
    def validate_max_continuous_leave_days(self):
        leave_max_days = frappe.get_doc("Leave Type", self.leave_type).max_continuous_days_allowed
        if float(self.total_leave_days > leave_max_days):
            frappe.throw("عدد ايام الاجازة المتتالي يجب ان يكون اقل من عدد الايام المخصصة لهذا النوع من الاجازات")

    # 6- add field Applicable After in Leave Type , allow employee make leave application after  (Working Days)
    def validate_leave_date_if_allow_after(self):
        applicable_after = frappe.get_doc("Leave Type", self.leave_type).applicable_after
        date_dif = date_diff(self.from_date, datetime.now())
        print('*' * 300)
        print(date_dif)
        if date_dif < applicable_after:
            frappe.throw(f'يجب التقديم للجازة {self.leave_type}'
                         f' قبل   {applicable_after}'
                         f'  ايام عمل'
                         )


@frappe.whitelist()
def get_total_leaves(employee, leave_type, from_date, to_date):
    if employee and leave_type and from_date and to_date:
        leave_allocations = frappe.db.sql(
            """ select name from `tabLeave Allocation` where employee = %s
        and leave_type = %s and from_date <= %s and to_date >= %s
        """, (employee, leave_type, from_date, to_date), as_dict=1)
        if leave_allocations:
            allocation_name = leave_allocations[0]
            allocation_doc = frappe.get_doc('Leave Allocation', allocation_name)
            allocation_days = allocation_doc.total_leaves_allocated
            return allocation_days
        else:
            return 0
    else:
        return


@frappe.whitelist()
def get_total_leave_days(from_date, to_date):
    return date_diff(to_date, from_date) + 1
