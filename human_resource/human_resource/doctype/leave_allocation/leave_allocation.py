# Copyright (c) 2023, mohammed and contributors
# For license information, please see license.txt
from datetime import datetime

# import frappe
from frappe.model.document import Document
from frappe.utils import date_diff
import frappe


class LeaveAllocation(Document):
    def before_save(self):
        self.validate_if_from_date_after_to_date()
        self.get_previous_from_and_to_dates()
        self.check_is_there_interfere()

    # 3- Add Validate when create or save Leave Allocation  if from date value  after to date
    # value and if already  have allocation to same Dates , Employee and leave Type

    def validate_if_from_date_after_to_date(self):
        date_dif = date_diff(self.to_date, self.from_date)
        if date_dif < 0:
            frappe.throw('خطا, تاريخ نهاية الاجازة يجب ان يكون بعد تاريخ البداية')

    def check_is_there_interfere(self):
        previous_dates = self.get_previous_from_and_to_dates()
        is_date_interfere = False

        for date in previous_dates:
            is_date_interfere = self.is_dates_interfere(date.from_date, date.to_date)
            if is_date_interfere and self.name != date.name:
                frappe.throw(
                    " هناك تتداخل بين فترة هذه الإجازة مع فترة اجازة اخرى من نفس النوع لنفس الموظف"
                    f"{datetime.strftime(date.from_date, '%Y-%b-%d')} "
                    f"to {datetime.strftime(date.to_date, '%Y-%b-%d')}")

    def is_dates_interfere(self, from_date, to_date):
        is_date_interfere = False
        current_from_date = datetime.strptime(self.from_date, '%Y-%m-%d').date()
        current_to_date = datetime.strptime(self.to_date, '%Y-%m-%d').date()
        previous_from_date = from_date
        previous_to_date = to_date
        if previous_from_date <= current_from_date <= previous_to_date:
            is_date_interfere = True
        elif previous_from_date <= current_to_date <= previous_to_date:
            is_date_interfere = True
        elif previous_from_date >= current_from_date and previous_to_date <= current_to_date:
            is_date_interfere = True
        elif previous_from_date <= current_from_date and previous_to_date >= current_to_date:
            is_date_interfere = True

        return is_date_interfere

    def get_previous_from_and_to_dates(self):

        dates = frappe.db.sql(
            """ select name, from_date , to_date from `tabLeave Allocation` where leave_type = %s and employee = %s  """
            , (self.leave_type, self.employee), as_dict=1)

        print('*' * 200)
        print(dates)
        return dates

        # [{'from_date': datetime.date(2023, 1, 1), 'to_date': datetime.date(2023, 12, 31)}]
