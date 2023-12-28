import frappe

def validate_default_disbursement_account(doc, method=None):
    if doc.default_disbursement_account:
        account = frappe.get_doc("Bank Account", doc.default_disbursement_account)
        if account.company != doc.company_name:
            frappe.throw(f"Account Should Belong to the Same Company")
