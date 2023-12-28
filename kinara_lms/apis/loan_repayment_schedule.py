import frappe

@frappe.whitelist()
def get_loan_repayment_schedule(**kwargs):
	doc_names = frappe.db.get_list("Loan Repayment Schedule", filters={'loan': kwargs["loan"]})
	response = []
	for name in doc_names:
		doc = frappe.get_doc("Loan Repayment Schedule",name["name"])
		response.append({
			"name": doc.name, 
			"loan": doc.loan, 
			"loan_disbursement": doc.loan_disbursement, 
			"company": doc.company, 
			"loan_restructure": doc.loan_restructure, 
			"loan_amount": doc.loan_amount, 
			"disbursed_amount": doc.disbursed_amount, 
			"rate_of_interest": doc.rate_of_interest, 
			"posting_date": doc.posting_date, 
			"adjusted_interest": doc.adjusted_interest, 
			"loan_product": doc.loan_product, 
			"repayment_frequency": doc.repayment_frequency, 
			"repayment_schedule_type": doc.repayment_schedule_type, 
			"repayment_date_on": doc.repayment_date_on, 
			"repayment_method": doc.repayment_method, 
			"repayment_periods": doc.repayment_periods, 
			"monthly_repayment_amount": doc.monthly_repayment_amount, 
			"repayment_start_date": doc.repayment_start_date, 
			"moratorium_tenure": doc.moratorium_tenure, 
			"treatment_of_interest": doc.treatment_of_interest, 
			"status": doc.status,
			"count_of_emi": len(doc.repayment_schedule)
        })
	return response
		
    