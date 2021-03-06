import frappe

@frappe.whitelist(allow_guest=True)
def get_todos():
    # doc = frappe.get_doc('Todo')
    doc = frappe.db.get_all('ToDo', fields=["description", "status", "creation"])
    return {
        "ok": True,
        "statusCode": 200,
        "data": doc,
    }