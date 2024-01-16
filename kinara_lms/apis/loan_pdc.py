import frappe
import json
from datetime import datetime

@frappe.whitelist()
def update_bulk_loan_pdc(**kwargs):
	allowed_fields = ["status","document_link"]
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
			doc = frappe.get_doc("Loan PDC",data["name"])
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
def get_short_pdc(**kwargs):
	short_pdc = []
	ach_not_present_and_repayment_schedule_not_present = get_ach_not_present_and_repayment_schedule_not_present()
	short_pdc.extend(ach_not_present_and_repayment_schedule_not_present)
	active_and_presented_pdc = get_active_and_presented_pdc()
	active_and_presented_pdc_dict = {d["lrs"]: sorted(d["rs_payment_date"].split(','), key=lambda x: datetime.strptime(x, "%Y-%m-%d")) for d in active_and_presented_pdc}
	mapped_and_unmapped_pdc = get_mapped_and_unmapped_pdc()
	for pdc in mapped_and_unmapped_pdc:
		pdc["rs_payment_date"] = sorted(pdc["rs_payment_date"].split(','), key=lambda x: datetime.strptime(x, "%Y-%m-%d"))
		pdc["rs_payment_date"] = pdc["rs_payment_date"][pdc["tip"]:]
		result_list = pdc["rs_payment_date"]
		if pdc["lrs"] in active_and_presented_pdc_dict.keys():
			result_list = [payment_date for payment_date in pdc["rs_payment_date"] if payment_date not in active_and_presented_pdc_dict[pdc["lrs"]]]
		pdc["result_list"] = result_list
		pdc["Count of Short PDC"] = len(result_list)
		if len(result_list) > 0:
			pdc["Next Due Date for which PDC is not available"] = result_list[0]
		else:
			pdc["Next Due Date for which PDC is not available"] = None
		pdc.pop('lrs', None)
		pdc.pop('tip', None)
		pdc.pop('rs_payment_date', None)
		pdc.pop('result_list', None)
	short_pdc.extend(mapped_and_unmapped_pdc)
	return short_pdc
		
def get_ach_not_present_and_repayment_schedule_not_present():
	ach_not_present_and_repayment_schedule_not_present = frappe.db.sql("""SELECT loan.name as "Loan", 
																		loan.applicant as "Customer URN", 
																		entity.customer_name as "Business Entity Name", 
																		"" as "Count of short PDC", 
																		"" as "Next Due Date for which PDC is not available"
																		FROM `tabLoan` as loan
																		LEFT JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
																		LEFT JOIN `tabCustomer` as entity ON entity.name = loan.applicant
																		WHERE loan.name NOT IN (SELECT ln.name
																								FROM `tabLoan` as ln
																								JOIN `tabLoan ACH` as loan_ach ON ln.name = loan_ach.loan) AND lrs.name IS NULL """, as_dict = True)
	return ach_not_present_and_repayment_schedule_not_present

def get_active_and_presented_pdc():
	active_and_presented_pdc = frappe.db.sql("""SELECT lrs.name as "lrs", 
										  		GROUP_CONCAT(rs.payment_date) as "rs_payment_date"
												FROM `tabLoan` as loan
												JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name AND lrs.status = "Active"
												JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
												JOIN `tabLoan PDC` as pdc 
												ON pdc.emi = rs.name 
												AND pdc.loan = loan.name 
												AND pdc.loan_repayment_schedule = lrs.name
										  		AND (pdc.status = "Active" OR pdc.status = "Presented")
										  		GROUP BY lrs.name
												""", as_dict = True)
	return active_and_presented_pdc

def get_mapped_and_unmapped_pdc():
	mapped_and_unmapped_pdc = frappe.db.sql("""SELECT loan.name as "loan", 
												lrs.name as "lrs", 
												lrs.total_installments_paid as "tip",
												GROUP_CONCAT(rs.payment_date) as "rs_payment_date",
										 		loan.applicant as "Customer URN", 
												entity.customer_name as "Business Entity Name" 
												FROM `tabLoan` as loan
												JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
												JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
										 		LEFT JOIN `tabCustomer` as entity ON entity.name = loan.applicant
												LEFT JOIN `tabLoan PDC` as pdc 
												ON pdc.emi = rs.name 
												AND pdc.loan = loan.name 
												AND pdc.loan_repayment_schedule = lrs.name
												GROUP BY lrs.name
												""", as_dict = True)
	return mapped_and_unmapped_pdc