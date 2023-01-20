# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe

from frappe.model.document import Document


class Employee(Document):
    def validate(self):
        self.calculate_age()
        self.age_lower_sixty()
        self.full_name()
        self.mobile_validation()
        self.child_table_length()

    def calculate_age(self):
        dob = datetime.strptime(self.employee_date_of_birth, '%Y-%m-%d').date()
        now = datetime.now()
        age = now.year - dob.year
        self.employee_age = age

    def age_lower_sixty(self):
        age = int(self.employee_age)
        status = self.employee_status
        if age >= 60 and status == 'Active':
            frappe.throw('Active employee age must be lower than 60')

    def full_name(self):
        first = self.employee_first_name if self.employee_first_name is not None else ""
        middle = self.employee_middle_name if self.employee_middle_name is not None else ""
        last = self.employee_last_name if self.employee_last_name is not None else ""
        self.employee_full_name = first + ' ' + middle + ' ' + last

    def mobile_validation(self):
        mobile = self.employee_mobile if self.employee_mobile is not None else ""
        if len(mobile) < 10:
            frappe.throw('mobile number must be more than 9 digits')
        elif not mobile.startswith('059'):
            frappe.throw('Mobile number must start with 059')

    def child_table_length(self):
        if len(self.employee_education) < 2:
            frappe.throw('the employee must have more than two education degrees')
