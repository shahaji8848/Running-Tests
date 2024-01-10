import frappe

def created_loan_related_docs(doc, method=None):
	for d in doc.get("entities") or []:
		frappe.get_doc({
			"doctype": "Loan Entity Mapping",
			"loan": doc.name,
			"entity": d.get("entity"),
			"entity_relationship_type": d.get('entity_relationship_type')
		}).insert()
	
	for d in doc.get("loan_documents") or []:
		frappe.get_doc({
			"doctype": "Loan Documents",
			"loan": doc.name,
			"document_type": doc.name,
			"document_details": d.get("document_details")
		}).insert()

	for d in doc.get("insurance_details") or []:
		insurance_doc = frappe.new_doc("Loan Insurance")
		insurance_doc.loan = doc.name
		insurance_doc.insurer_entity_id = d.get("insurer_entity_id")
		insurance_doc.insurer_entity_type = d.get("insurer_entity_type")
		insurance_doc.insurer_urn = d.get("insurer_urn")
		insurance_doc.insurance_id = d.get("insurance_id")
		insurance_doc.insurance_premium = d.get("insurance_premium")
		insurance_doc.insured_amount = d.get("insured_amount")
		insurance_doc.nominee_urn = d.get("nominee_urn")
		insurance_doc.nominee_name = d.get("nominee_name")
		insurance_doc.relationship = d.get("relationship")
		insurance_doc.date_of_birth = d.get("date_of_birth")
		insurance_doc.start_date = d.get("start_date")
		insurance_doc.end_date = d.get("end_date")
		insurance_doc.save()

	for d in doc.get("disbursement_details") or []:
		disbursement_doc = frappe.new_doc("Loan Disbursement")
		disbursement_doc.against_loan = doc.name
		disbursement_doc.disbursement_date= d.get("actual_disbursement_date")
		disbursement_doc.reference_date= d.get("scheduled_disbursement_date")
		disbursement_doc.disbursed_amount= d.get("disbursement_amount")
		disbursement_doc.bank_account = d.get("disbursement_account")
		disbursement_doc.customer_bank_account_number = d.get("customer_bank_account_number")
		disbursement_doc.customer_bank_ifsc_code = d.get("customer_bank_ifsc_code")
		disbursement_doc.customer_bank_name = d.get("customer_bank_name")
		disbursement_doc.customer_bank_branch_name = d.get("customer_bank_branch_name")
		disbursement_doc.customer_bank_account_holder_name = d.get("customer_bank_account_holder_name")
		disbursement_doc.disbursement_mode = d.get("disbursement_mode")
		disbursement_doc.save()

	if doc.get("collateral_details"):
		loan_security_assignment = frappe.new_doc("Loan Security Assignment")
		loan_security_assignment.applicant_type = doc.get("applicant_type")
		loan_security_assignment.applicant = doc.get("applicant")
		loan_security_assignment.security_owner_type = doc.get("collateral_owner_type")
		loan_security_assignment.security_owner = doc.get("collateral_owner")

		for d in doc.get("collateral_details") or []:
			loan_security_assignment.append("securities", {
				"loan_security": d.get("collateral_id"),
				"qty": 1,
				"loan_security_price": frappe.db.get_value("Loan Security", d.get("collateral_id"), "original_security_value"),
			})

		loan_security_assignment.insert()

		loan_security_assignment.append("allocated_loans", {
			"loan": doc.name
		})

		loan_security_assignment.save()
		loan_security_assignment.submit()


def override_name(doc, method=None):
	doc.name = doc.get("loan_account_number")


def validate_customer_type(doc, method=None):
	if frappe.db.get_value('Customer', doc.applicant, 'customer_type') == "Individual":
		frappe.throw(f"Entity Type Cannot Be Individual: {doc.applicant}")

	if doc.custom_individual_applicant:
		if frappe.db.get_value('Customer', doc.custom_individual_applicant, 'customer_type') != "Individual":
			frappe.throw(f"Applicant Type Should Be Individual: {doc.custom_individual_applicant}")

	for co_applicant in doc.custom_co_applicants:
		if frappe.db.get_value('Customer', co_applicant.co_applicant, 'customer_type') != "Individual":
			frappe.throw(f"Co Applicant Type Should Be Individual: {co_applicant.co_applicant}")

		if hasattr(doc,'insurance_details'):
			for insurance_details in doc.insurance_details:
				if insurance_details.get('insurer_urn') not in [co_applicant.co_applicant,doc.custom_individual_applicant]:
					frappe.throw("Same should be Applicant/Co-applicant URN's and Insurer urn")

	for guarantor in doc.custom_guarantors:
		if frappe.db.get_value('Customer', guarantor.guarantors, 'customer_type') != "Individual":
			frappe.throw(f"Gurantor Type Should Be Individual: {guarantor.guarantors}")