import frappe



@frappe.whitelist()
def get_default_disbursement_account(**kwargs):
	doc = frappe.get_doc("Company", kwargs["Company Name"])
	if not doc.default_disbursement_account:
		frappe.throw("No Default Disbursement Account Found")
	doc = frappe.get_doc("Bank Account", doc.default_disbursement_account)
	return doc

@frappe.whitelist()
def bank_account():
	data = frappe.db.sql("""
		SELECT
			bap.name as bank_account_purpose,
			ba.*
			
		FROM `tabBank Account` ba
		left JOIN `tabBank Account Purpose` bap
		ON ba.name = bap.value
	""", as_dict=1)
	return data
