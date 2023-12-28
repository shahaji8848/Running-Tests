import frappe

@frappe.whitelist()
def get_loan_disbursement_invoices(urn):
    if urn != None:
        values = {'urn': urn}
        data = frappe.db.sql("""
            SELECT
                *
            FROM `tabDisbursement Invoice Detail`
            WHERE buyer_urn = %(urn)s
        """, values=values, as_dict=1)
        return data