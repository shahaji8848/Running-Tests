import frappe


def validate_loan_product_code(doc, method=None):
	if doc.product_code:
		if len(doc.product_code) > 6: 
			frappe.throw("Loan Product Code cannot have more than 6 characters")
		elif len(doc.product_code) < 3: 
			frappe.throw("Loan Product Code cannot have less than 3 characters")
		elif not doc.product_code.isalnum(): 
			frappe.throw("Loan Product Code cannot have spaces or special characters")
