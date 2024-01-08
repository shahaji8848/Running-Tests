import frappe
import json

@frappe.whitelist()
def update_bulk_loan_ach(**kwargs):
	allowed_fields = ["umrn_no","reference_1","primary_mobile_number","reference_2","document_link", "sponsor_bank_code", "utility_code", "email_id", "docstatus"]
	response = {
		"data": []
    }
	body = json.loads(frappe.request.data)
	for data in body["data"]:
		response_dict = {
			"status" : "",
		}
		try:
			if "name" not in data:
				frappe.throw("Record Name Is Mandatory")
			doc = frappe.get_doc("Loan ACH",data["name"])
			for key in data.keys():
				if key in allowed_fields:
					doc.set(key, data[key])
			doc.save()
			response_dict["name"] = doc.name
			response_dict["status"] = "success"
			response_dict["message"] = "record updated"
			response_dict["doc"] = doc
		except Exception as e:
			response_dict["status"] = "error"
			response_dict["message"] = e
		response["data"].append(response_dict)
	return response

@frappe.whitelist()
def get_mandate_details_ach_not_active(**kwargs):
    
	conditions = []
	if "applicant_name" in kwargs and kwargs["applicant_name"] != "":
		conditions.append(f"""individual_applicant.customer_name = '{kwargs["applicant_name"]}'""")
	if "business_name" in kwargs and kwargs["business_name"] != "":
		conditions.append(f"""entity.customer_name = '{kwargs["business_name"]}'""")
	if "ach_registration_number" in kwargs and kwargs["ach_registration_number"] != "":
		conditions.append(f"""ach.ach_registration_number = '{kwargs["ach_registration_number"]}'""")
		
	where_clause = "WHERE " + " AND ".join(conditions)
	ach_details  = frappe.db.sql(f"""SELECT COALESCE(NULLIF(co_lending_partner.partner_name,''), NULLIF(loan_channel_partner.name1,''), loan.company) as "partner_name",
									ach.ach_registration_date as "Mandate Date",
									ach.sponsor_bank_code as "Sponsor Bank Code",
									ach.utility_code as "Utility Code",
									loan.company as "Name of Utility/Biller/Bank/Company",
									ach.account_type as "Ac Type",
									ach.bank_account_number as "Legal Account Number",
									CASE
    									WHEN ach.branch_name IS NOT NULL AND ach.branch_name != ''
        									THEN CONCAT_WS(', ', ach.bank_name, ach.branch_name)
										ELSE ach.bank_name
									END AS "Name of the Destination bank with Branch",
									ach.ifsc_code as "IFSC Code / Micr Code",
									ach.max_ach_amount as "Debit Amt of/Upto Maximum Amt",
									loan.name as "Consumer Reference Number",
									loan.applicant as "Scheme/Plan Reference No",
									ach.frequency as "Frequency",
									ach.ach_start_date as "Start Date",
									ach.ach_end_date as "End Date",
									ach.account_holder_name as "Account Holder Name",
									entity.mobile_no as "Mobile No",
									entity.email_id as "E Mail ID",
									ach.umrn_no as "UMRN No",
									ach.docstatus as "Mandate Status",
									ach.rejection_code as "Rejection Code",
									ach.rejection_reason as "Rejection Reason",
									ach.initial_reject_reason as "Initial Reject Reason",
									ach.processed_on_with_umrn as "Processed On With UMRN",
									ach.bank_account_number as "bank_account_number",
									COALESCE(NULLIF(loan.co_lending_partner,''), NULLIF(loan.custom_channel_partner,''), loan.company) as "partner_code"
									FROM `tabLoan ACH` as ach
									JOIN `tabLoan` as loan ON loan.name = ach.loan
									LEFT JOIN `tabCustomer` as entity ON entity.name = loan.applicant
							  		LEFT JOIN `tabCustomer` as individual_applicant ON individual_applicant.name = loan.custom_individual_applicant
									LEFT JOIN `tabLoan Partner` as co_lending_partner ON co_lending_partner.name = loan.co_lending_partner
									LEFT JOIN `tabLoan Channel Partner` as loan_channel_partner ON loan_channel_partner.name = loan.custom_channel_partner
                                    {where_clause}
                                    """, as_dict=1)
    
	response = []
	for ach in ach_details:
		response_doc = {
            "partner_name" : ach["partner_name"],
            "Mandate Date": ach["Mandate Date"],
            "Sponsor Bank Code": ach["Sponsor Bank Code"],
            "Utility Code": ach["Utility Code"],
            "Name of Utility/Biller/Bank/Company": ach["Name of Utility/Biller/Bank/Company"],
            "Ac Type": ach["Ac Type"],
            "Legal Account Number": ach["Legal Account Number"],
            "Name of the Destination bank with Branch": ach["Name of the Destination bank with Branch"],
            "IFSC Code / Micr Code": ach["IFSC Code / Micr Code"],
            "Debit Amt of/Upto Maximum Amt": ach["Debit Amt of/Upto Maximum Amt"],
            "Amount": None,
            "Consumer Reference Number": ach["Consumer Reference Number"],
            "Scheme/Plan Reference No": ach["Scheme/Plan Reference No"],
            "Frequency": ach["Frequency"],
            "Start Date": ach["Start Date"],
            "End Date": ach["End Date"],
            "Account Holder Name": ach["Account Holder Name"],
            "Customer Additional Information": None,
            "Telephone No": None,
            "Mobile Number": ach["Mobile Number"],
            "E Mail ID": ach["E Mail ID"],
            "Category Code": None,
			"UMRN No" : ach["UMRN No"],
            "Mandate Status": ach["Mandate Status"],
            "Rejection Code": ach["Rejection Code"],
            "Rejection Reason": ach["Rejection Reason"],
            "Initial Reject Reason": ach["Initial Reject Reason"],
            "Processed On With UMRN": ach["Processed On With UMRN"],
            "bank_account_number": ach["bank_account_number"],
            "partner_code": ach["partner_code"],
        }
		response.append(response_doc)
	return response

		