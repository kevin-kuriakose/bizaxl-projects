import frappe
from frappe.model.document import Document


class BATask(Document):
    def validate(self):
        self.validate_dependencies()

    def validate_dependencies(self):
        for dep in (self.depends_on or []):
            if dep.task == self.name:
                frappe.throw("A task cannot depend on itself.")

    def on_update(self):
        self.update_project_percent()

    def update_project_percent(self):
        if self.project:
            project = frappe.get_doc("BA Project", self.project)
            if project.percent_complete_method == "Task Completion":
                project.update_percent_complete()
                project.db_update()
