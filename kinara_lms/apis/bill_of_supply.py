import frappe
import json


@frappe.whitelist()
def get_bill_of_supply_pdf(**kwargs):
    body = json.loads(frappe.request.data)
    doc = frappe.new_doc('Bill of Supply')
    doc.loan_id = body["loan"]
    loan_installment_date = body["demand_date"].split('-')
    doc.loan_installment_date = loan_installment_date[2]+"-"+loan_installment_date[1]+"-"+loan_installment_date[0]
    doc.save()
    frappe.db.commit()
    base_url = frappe.utils.get_url()
    pdf_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Bill%20of%20Supply&name={doc.name}&format=Bill%20of%20Supply&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en"
    return{"pdf": pdf_url}