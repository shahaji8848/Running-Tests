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
	pdc_not_mapped = frappe.db.sql("""SELECT DISTINCT loan.name as "Loan", 
											   		loan.applicant as "Customer URN", 
											   		entity.customer_name as "Business Entity Name", 
											   		COUNT(rs.name)-lrs.total_installments_paid as "Count of short PDC", 
											   		GROUP_CONCAT(rs.payment_date) as "Next Due Date", 
											   		lrs.total_installments_paid as "Total Installment Paid",
													FROM `tabLoan` as loan
													JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
													JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
													LEFT JOIN `tabLoan PDC` as pdc ON pdc.emi = rs.name 
											   										AND pdc.loan = loan.name 
											   										AND pdc.loan_repayment_schedule = lrs.name 
											   										AND pdc.status != "Active"
													LEFT JOIN `tabCustomer` as entity
													ON entity.name = loan.applicant
													WHERE lrs.status = "Active"
													GROUP BY rs.parent""", as_dict = True)
	
	
	pdc_not_mapped_or_not_present = frappe.db.sql("""SELECT DISTINCT loan.name as "Loan", 
											   		loan.applicant as "Customer URN", 
											   		entity.customer_name as "Business Entity Name", 
											   		COUNT(rs.name)-lrs.total_installments_paid as "Count of short PDC", 
											   		GROUP_CONCAT(rs.payment_date) as "Next Due Date", 
											   		lrs.total_installments_paid as "Total Installment Paid",
													FROM `tabLoan` as loan
													JOIN `tabLoan Repayment Schedule` as lrs ON lrs.loan = loan.name
													JOIN `tabRepayment Schedule` as rs ON rs.parent = lrs.name
													LEFT JOIN `tabLoan PDC` as pdc ON pdc.emi = rs.name 
											   										AND pdc.loan = loan.name 
											   										AND pdc.loan_repayment_schedule = lrs.name 
											   										AND pdc.status != "Active"
													LEFT JOIN `tabCustomer` as entity
													ON entity.name = loan.applicant
													WHERE lrs.status = "Active"
													GROUP BY rs.parent""", as_dict = True)
	for record in pdc_not_mapped_or_not_present:
		date_objects = [datetime.datetime.strptime(date, "%Y-%m-%d").date() for date in record["Next Due Date"].split(",")]
		sorted_dates = sorted(date_objects)
		try:
			record["Next Due Date for which PDC is not available"] = sorted_dates[record["Total Installment Paid"]]
		except Exception as e:
			record["Next Due Date for which PDC is not available"] = None
		record.pop("Next Due Date", None)
		record.pop("Total Installment Paid", None)
	
	short_pdc.append(pdc_not_mapped_or_not_present)

	return short_pdc
		