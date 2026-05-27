import frappe
def execute(filters=None):
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Timesheet", "fieldtype": "Link", "options": "BA Timesheet", "width": 160},
        {"fieldname": "employee", "label": "Employee", "fieldtype": "Link", "options": "BA Employee", "width": 140},
        {"fieldname": "project", "label": "Project", "fieldtype": "Link", "options": "BA Project", "width": 160},
        {"fieldname": "start_date", "label": "Date", "fieldtype": "Date", "width": 100},
        {"fieldname": "total_hours", "label": "Hours", "fieldtype": "Float", "width": 90},
        {"fieldname": "total_billable_hours", "label": "Billable Hrs", "fieldtype": "Float", "width": 110},
        {"fieldname": "total_billed_amount", "label": "Billed Amount", "fieldtype": "Currency", "width": 130},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 90},
    ]
    conditions = "WHERE docstatus = 1"
    values = {}
    if filters.get("employee"):
        conditions += " AND employee = %(employee)s"
        values["employee"] = filters["employee"]
    if filters.get("project"):
        conditions += " AND project = %(project)s"
        values["project"] = filters["project"]
    if filters.get("from_date"):
        conditions += " AND start_date >= %(from_date)s"
        values["from_date"] = filters["from_date"]
    if filters.get("to_date"):
        conditions += " AND start_date <= %(to_date)s"
        values["to_date"] = filters["to_date"]
    data = frappe.db.sql(f"""
        SELECT name, employee, project, start_date,
               total_hours, total_billable_hours, total_billed_amount, status
        FROM `tabBA Timesheet`
        {conditions}
        ORDER BY start_date DESC
    """, values, as_dict=True)
    return columns, data
