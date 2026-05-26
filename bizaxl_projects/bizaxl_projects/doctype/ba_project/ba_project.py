import frappe
from frappe.model.document import Document
from frappe.utils import flt


class BAProject(Document):
    def validate(self):
        self.update_percent_complete()
        self.calculate_margin()

    def update_percent_complete(self):
        if self.percent_complete_method == "Task Completion":
            tasks = frappe.get_all("BA Task",
                filters={"project": self.name},
                fields=["status"])
            if tasks:
                completed = len([t for t in tasks if t.status == "Completed"])
                self.percent_complete = round((completed / len(tasks)) * 100, 2)

    def calculate_margin(self):
        if self.total_billing_amount and self.total_costing_amount:
            self.gross_margin = flt(self.total_billing_amount) - flt(self.total_costing_amount)
            if self.total_billing_amount:
                self.per_gross_margin = round(
                    (self.gross_margin / self.total_billing_amount) * 100, 2
                )
