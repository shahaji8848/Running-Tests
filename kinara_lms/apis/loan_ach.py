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
		