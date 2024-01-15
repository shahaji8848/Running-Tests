import frappe
import json


@frappe.whitelist()
def get_preclosure_foreclosure_pdf(**kwargs):
    body = json.loads(frappe.request.data)
    proposed_closure_date = body["as_on_date"].split("-")
    doc_list = frappe.db.get_list('Preclosure-Foreclosure Report',
    filters={
        'loan_account_number': body["loan"],
        'proposed_closure_date': proposed_closure_date[2]+"-"+proposed_closure_date[1]+"-"+proposed_closure_date[0]

    })
    if len(doc_list) > 0:
        doc = frappe.get_doc('Preclosure-Foreclosure Report', doc_list[0]['name'])
    else:
        doc = frappe.new_doc('Preclosure-Foreclosure Report')
        doc.loan_account_number = body["loan"]
        proposed_closure_date = body["as_on_date"].split("-")
        doc.proposed_closure_date = proposed_closure_date[2]+"-"+proposed_closure_date[1]+"-"+proposed_closure_date[0]
        doc.save()
        frappe.db.commit()
    base_url = frappe.utils.get_url()
    pdf_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Preclosure-Foreclosure%20Report&name={doc.name}&format=Loan%20Preclosure%20Foreclosure&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en"
    return{"pdf": pdf_url}