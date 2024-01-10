import frappe
import json


@frappe.whitelist()
def update_bank_account(**kwargs):
    allowed_fields = ["account_name","account","bank","account_type","account_subtype","custom_account_purpose","disabled","is_default""is_company_account","company","party_type","party","iban","branch_code","custom_ifsc_code","bank_account_no","integration_id","last_integration_date","mask"]
    data = json.loads(frappe.request.data)    
    response_dict = {
        "status" : "",
    }
    try:
        if "name" not in data:
            frappe.throw("Record Name Is Mandatory")
        doc = frappe.get_doc("Bank Account",data["name"])
        for key in data.keys():
            if data[key] is not None:
                if key in allowed_fields:
                    doc.set(key, data[key])
        doc.save()
        if "bank_account_no" in data.keys() and data["bank_account_no"] is not None:
            if data["bank_account_no"] != doc.name:
                frappe.rename_doc("Bank Account", data["name"], data["bank_account_no"], merge=False)
                doc = frappe.get_doc("Bank Account",data["bank_account_no"])
        response_dict["name"] = doc.name
        response_dict["status"] = "success"
        response_dict["message"] = "record updated"
        response_dict["doc"] = doc
        frappe.db.commit()
    except Exception as e:
        frappe.db.rollback()
        response_dict["status"] = "error"
        response_dict["message"] = e
    return response_dict
