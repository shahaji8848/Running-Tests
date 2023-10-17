import frappe

def created_loan_related_docs(doc, method=None):
	for d in doc.get("entities"):
		frappe.get_doc({
			"doctype": "Loan Entity Mapping",
			"loan": doc.name,
			"entity": d.get("entity")
		}).insert()
	
	for d in doc.get("loan_documents"):
		frappe.get_doc({
			"doctype": "Loan Documents",
			"loan": doc.name,
			"document_type": doc.name,
			"document_details": d.get("document_details")
		}).insert()