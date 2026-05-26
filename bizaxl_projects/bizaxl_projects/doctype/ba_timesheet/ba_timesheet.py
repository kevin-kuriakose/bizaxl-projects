import frappe
from frappe.model.document import Document
from frappe.utils import flt, time_diff_in_hours


class BATimesheet(Document):
    def validate(self):
        self.calculate_totals()
        self.set_employee_name()

    def set_employee_name(self):
        if self.employee:
            self.employee_name = frappe.get_value(
                "BA Employee", self.employee, "employee_name"
            )

    def calculate_totals(self):
        total_hours = 0
        total_billing = 0
        total_costing = 0

        for log in self.time_logs:
            # Calculate hours from from_time/to_time if not set
            if log.from_time and log.to_time and not log.hours:
                log.hours = round(
                    time_diff_in_hours(log.to_time, log.from_time), 2
                )
            # Calculate amounts
            log.billing_hours = log.billing_hours or log.hours
            log.billing_amount = flt(log.billing_hours) * flt(log.billing_rate)
            log.costing_amount = flt(log.hours) * flt(log.costing_rate)

            total_hours += flt(log.hours)
            total_billing += log.billing_amount
            total_costing += log.costing_amount

        self.total_hours = total_hours
        self.total_billing_amount = total_billing
        self.total_costing_amount = total_costing

    def on_submit(self):
        self.status = "Submitted"
        self.update_task_actual_time()

    def update_task_actual_time(self):
        for log in self.time_logs:
            if log.task:
                current = frappe.get_value("BA Task", log.task, "actual_time") or 0
                frappe.db.set_value("BA Task", log.task, "actual_time",
                                    flt(current) + flt(log.hours))
