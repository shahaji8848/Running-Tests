import frappe
import json


@frappe.whitelist()
def get_bill_of_supply_pdf(**kwargs):
    loan = kwargs["loan"]
    demand_date = kwargs['demand_date']
    demand_type = kwargs['demand_type']
    if demand_type not in ["EMI","Charges"]:
        return {"error:":"Invalid Demand Type - Accepted Demand Types are EMI/Charges"}
    bs_list = frappe.db.sql(f"""SELECT bs.name as "name"
                                FROM `tabBill of Supply` AS bs
                                WHERE
                                    bs.loan_id = "{loan}"
                                    AND bs.posting_date = "{demand_date}"
                                    AND bs.demand_type = "{demand_type}"
                                    AND bs.docstatus = 1
                                """, as_dict = True)
    pdf = []
    base_url = frappe.utils.get_url()
    for bs in bs_list:
        pdf_url = f"{base_url}/api/method/frappe.utils.print_format.download_pdf?doctype=Bill%20of%20Supply&name={bs['name']}&format=Bill%20of%20Supply&no_letterhead=1&letterhead=No%20Letterhead&settings=%7B%7D&_lang=en"
        pdf.append(pdf_url)
    return pdf