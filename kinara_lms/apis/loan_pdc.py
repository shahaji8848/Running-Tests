import frappe
import json
import datetime

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
	short_pdc.append(ach_not_present_and_repayment_schedule_not_present)
	active_and_presented_pdc = frappe.db.sql("""SELECT lrs.name as "lrs", 
										  		rs.idx as "rs_idx"
												FROM `tabLoan` as loan
												JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
												JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
												LEFT JOIN `tabLoan PDC` as pdc 
												ON pdc.emi = rs.name 
												AND pdc.loan = loan.name 
												AND pdc.loan_repayment_schedule = lrs.name
										  		AND (pdc.status = "Active" OR pdc.status = "Presented")
												""", as_dict = True)
	active_and_presented_pdc_dict = {d["lrs"]: sorted(d["rs_idx"].split(','), key=lambda x: int(x)) for d in active_and_presented_pdc}

	mapped_and_unmapped_pdc = frappe.db.sql("""SELECT loan.name as "loan", 
												lrs.name as "lrs", 
												lrs.total_installments_paid as "tip",
												GROUP_CONCAT(rs.idx) as "rs_idx",
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
	for pdc in mapped_and_unmapped_pdc:
		pdc["rs_idx"] = sorted(pdc["rs_idx"].split(','), key=lambda x: int(x))
		pdc["rs_idx"] = pdc["rs_idx"][pdc["tip"]:]
		result_list = [num for num in pdc["rs_idx"] if num not in active_and_presented_pdc_dict[pdc["lrs"]]]
		pdc["Count of Short PDC"] = len(result_list)
		if len(result_list) > 0:
			next_due_date = frappe.db.sql(f"""SELECT rs.payment_date as "Payment Date"
												FROM `tabLoan` as loan
												JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
												JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
												WHERE loan.name = "{pdc["loan"]}"
												AND lrs.name = "{pdc["lrs"]}"
												AND rs.idx = "{result_list[0]}"
												""", as_dict = True)
			pdc["Next Due Date for which PDC is not available"] = next_due_date[0]["Payment Date"]
		else:
			pdc["Next Due Date for which PDC is not available"] = None

	
	short_pdc.append()

	return short_pdc
		