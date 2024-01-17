import frappe


def validate_loan_product_code(doc, method=None):
	if doc.product_code:
		if len(doc.product_code) > 6: 
			frappe.throw("Loan Product Code cannot have more than 6 characters")
		elif len(doc.product_code) < 3: 
			frappe.throw("Loan Product Code cannot have less than 3 characters")
		elif not doc.product_code.isalnum(): 
			frappe.throw("Loan Product Code cannot have spaces or special characters")
		elif doc.custom_maximum_spread_rate <= doc.custom_minimum_spread_rate:
			frappe.throw("Maximum Spread Rate Has to be more than Minimum Spread Rate")
		elif doc.maximum_loan_amount <= doc.custom_minimum_loan_amount:
			frappe.throw("Maximum Loan Amount Has to be more than Minimum Loan Amount")
		elif (doc.maximum_loan_amount < doc.custom_default_loan_amount) or (doc.custom_default_loan_amount < doc.custom_minimum_loan_amount):
			frappe.throw("Default Loan Amount Has to be between Minimum and Maximum Loan Amount")

		if 	doc.custom_maximum_tenure1 and doc.custom_minimum_tenure1:
			if doc.custom_maximum_tenure1 <  doc.custom_minimum_tenure1:
				frappe.throw("Maximum Tenure Has to be more than Minimum Tenure")

		if doc.custom_maximum_tenure1 and doc.custom_default_tenure1 and doc.custom_minimum_tenure1:
			if (doc.custom_maximum_tenure1 < doc.custom_default_tenure1) or (doc.custom_default_tenure1 < doc.custom_minimum_tenure1):
				frappe.throw("Default Tenure Has to be between Minimum and Maximum Tenure")		
