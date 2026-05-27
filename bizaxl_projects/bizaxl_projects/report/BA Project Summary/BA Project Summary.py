import frappe
from frappe.utils import flt
def execute(filters=None):
    filters = filters or {}
    columns = [
        {"fieldname": "name", "label": "Project", "fieldtype": "Link", "options": "BA Project", "width": 180},
        {"fieldname": "status", "label": "Status", "fieldtype": "Data", "width": 100},
        {"fieldname": "expected_start_date", "label": "Start", "fieldtype": "Date", "width": 100},
        {"fieldname": "expected_end_date", "label": "End", "fieldtype": "Date", "width": 100},
        {"fieldname": "percent_complete", "label": "% Complete", "fieldtype": "Float", "width": 100},
        {"fieldname": "total_tasks", "label": "Tasks", "fieldtype": "Int", "width": 80},
        {"fieldname": "total_hours", "label": "Hours Logged", "fieldtype": "Float", "width": 110},
        {"fieldname": "gross_margin", "label": "Gross Margin", "fieldtype": "Currency", "width": 130},
    ]
    conditions = "WHERE 1=1"
    values = {}
    if filters.get("status"):
        conditions += " AND p.status = %(status)s"
        values["status"] = filters["status"]
    if filters.get("company"):
        conditions += " AND p.company = %(company)s"
        values["company"] = filters["company"]
    data = frappe.db.sql(f"""
        SELECT p.name, p.status, p.expected_start_date, p.expected_end_date,
               p.percent_complete, p.gross_margin,
               COUNT(DISTINCT t.name) as total_tasks,
               COALESCE(SUM(ts.total_hours), 0) as total_hours
        FROM `tabBA Project` p
        LEFT JOIN `tabBA Task` t ON t.project = p.name
        LEFT JOIN `tabBA Timesheet` ts ON ts.project = p.name AND ts.docstatus = 1
        {conditions}
        GROUP BY p.name
        ORDER BY p.expected_end_date
    """, values, as_dict=True)
    return columns, data
