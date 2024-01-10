import frappe
from frappe.utils.data import flt

def on_update(doc,method=None):
    if doc.loan:
        set_individual_applicant_name_and_mobile_no(doc)
        if doc.loan_partner:
            set_loan_partner_address(doc)
        else:
            doc.loan_partner_address = None             
            doc.loan_partner_gstin = None
        set_company_billing_address(doc)
        set_company_amount_and_loan_partner_amount_values(doc)
        
    
def set_individual_applicant_name_and_mobile_no(doc):
    applicant = frappe.db.get_value('Loan',doc.loan,'custom_individual_applicant')
    if applicant:
        applicant_name, mobile_no = frappe.db.get_value('Customer', applicant, ['customer_name', 'mobile_no'])        
        if applicant_name:
            doc.custom_applicant_name = applicant_name
        if mobile_no:
            doc.custom_applicant_mobile_no = mobile_no

def set_company_billing_address(doc):
    company_gst_regime = frappe.db.get_value('Company', doc.company, 'gst_regime')
    result = None
    if company_gst_regime == "Decentralized":
        customer_state = frappe.db.get_value('Address', doc.customer_address, 'state')
        filter = f"""ads.state = "{customer_state}" """ #get company address matching customer's state
        result = execute_query(doc.company, filter, "Company")     #will return state if customer is present in company state
    if not result:
        filter = f"ads.is_primary_address = 1"          #get company primary address
        result = execute_query(doc.company, filter, "Company")     #will be used when regime is centralied or customer is not present in company state
    if len(result) > 0:
        doc.company_address = result[0]['name']          
        doc.company_gstin = result[0]['gstin']
    else:
        doc.company_address = None          
        doc.company_gstin = None

def set_loan_partner_address(doc,method=None):
    loan_partner_gst_regime = frappe.db.get_value('Loan Partner', doc.loan_partner, 'organization_type')
    result = None
    if loan_partner_gst_regime == "Decentralized":
        customer_state = frappe.db.get_value('Address', doc.customer_address, 'state')
        filter = f"""ads.state = "{customer_state}" """ #get loan partner address matching customer's state
        result = execute_query(doc.loan_partner, filter, "Loan Partner")     #will return state if customer is present in loan partner state
    if not result:
        filter = f"ads.is_primary_address = 1"          #get loan partner primary address
        result = execute_query(doc.loan_partner, filter, "Loan Partner")     #will be used when regime is centralied or customer is not present in loan partner state
    if len(result) > 0:
        doc.loan_partner_address = result[0]['name']          
        doc.loan_partner_gstin = result[0]['gstin']
    else:
        doc.loan_partner_address = None          
        doc.loan_partner_gstin = None


def execute_query(link_name, filter, link_doctype):
    conditions = f"""WHERE dl.parenttype = "Address" 
                    AND dl.parentfield = "links" 
                    AND dl.link_doctype = "{link_doctype}" 
                    AND dl.link_name = "{link_name}" 
                    AND {filter}"""
    result = frappe.db.sql(f"""SELECT ads.name, ads.gstin
                                FROM `tabAddress` as ads
                                JOIN `tabDynamic Link` as dl
                                ON ads.name = dl.parent
                                {conditions}
                                LIMIT 1""", as_dict = True)
    return result


def set_company_amount_and_loan_partner_amount_values(doc):
    if doc.loan_partner:
        loan_partner = frappe.get_doc('Loan Partner', doc.loan_partner)
        for item in doc.items:
            if len(loan_partner.shareables) == 0:
                item.ratio_percentage = 0
                item.loan_partner_amount = 0
            else:
                for row in loan_partner.shareables:
                    if item.item_code == row.shareable_type:
                        item.ratio_percentage = flt(row.partner_collection_percentage)
                        item.loan_partner_amount = (flt(item.amount)*flt(row.partner_collection_percentage))/100
                        break
                    else:
                        item.ratio_percentage = 0
                        item.loan_partner_amount = 0
    else:
        for item in doc.items:
            item.ratio_percentage = 0
            item.loan_partner_amount = 0
    for item in doc.items:
        item.company_amount = flt(item.amount) - flt(item.loan_partner_amount)