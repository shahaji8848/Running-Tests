import json

import frappe
from frappe.utils import cint

from lending.loan_management.doctype.loan_security_assignment.loan_security_assignment import (
	release_loan_security_assignment,
)


@frappe.whitelist()
def create_charge(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)
	
	charge = frappe.get_doc({
		"doctype": "Item",
		"item_code": args.charge_code,
		"item_name": args.charge_name,
		"gst_hsn_code": args.gst_hsn_code,
		"tax_inclusive": args.tax_inclusive,
		"item_defaults": [{
			"income_account": args.income_gl,
			"default_receivable_account": args.receivable_gl,
			"default_waiver_account": args.waiver_gl,
			"default_write_off_account": args.write_off_gl,
			"default_suspense_account": args.suspense_gl,
		}],
		"item_group": "Charges",
		"is_stock_item": 0,
	})

	if args.tax_applicable:
		charge.append("taxes", {"item_tax_template": "GST 18% - KCPL"})
	else:
		charge.is_nil_exempt = 1
	
	charge.insert()

	return charge


@frappe.whitelist()
def update_charge(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)
	
	charge = frappe.get_doc("Item", args.charge_code)

	if args.charge_name:
		charge.item_name = args.charge_name
	if args.gst_hsn_code:
		charge.gst_hsn_code = args.gst_hsn_code
	
	charge.tax_inclusive = cint(args.tax_inclusive)

	if "tax_applicable" in args:
		if args.tax_applicable:
			charge.is_nil_exempt = 0
			if not charge.taxes:
				charge.append("taxes", {"item_tax_template": "GST 18% - KCPL"})
		else:
			charge.is_nil_exempt = 1
			charge.taxes = []
	
	charge.save()

	return charge


@frappe.whitelist()
def create_collateral(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)
	
	loan_security = frappe.get_doc({
		"doctype": "Loan Security",
		"loan_security_code": args.collateral_id,
		"loan_security_name": args.collateral_name,
		"applicant_type": args.applicant_type,
		"applicant": args.applicant,
		"unit_of_measure": "Nos",
		"loan_security_type": args.loan_security_type,
		"loan_security_subtype": args.loan_security_subtype,
		"kinara_collateral_subtype": args.kinara_collateral_subtype,
		"original_security_value": args.collateral_value,
		"kinara_collateral_condition": args.kinara_collateral_condition,
		"kinara_description": args.kinara_description,
		"kinara_manufacturer_name": args.kinara_manufacturer_name,
		"kinara_model_number": args.kinara_model_number,
		"kinara_serial_number": args.kinara_serial_number,
		"kinara_cersai_charge_required": args.kinara_cersai_charge_required
	}).insert()

	return loan_security


@frappe.whitelist()
def get_collaterals_for_an_entity(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)

	res = []
	
	loan_security_assignments = frappe.db.get_all("Loan Security Assignment", {"applicant": args.applicant})

	for lsa in loan_security_assignments:
		sub_res = frappe._dict()

		lsa_doc = frappe.get_doc("Loan Security Assignment", lsa.name)
		collateral_id = lsa_doc.securities[0].loan_security
		sub_res.update({"collateral_id": collateral_id, "status": lsa_doc.status})

		collateral_fields = [
			"kinara_collateral_type",
			"kinara_collateral_subtype",
			"original_security_value",
			"utilized_security_value",
			"available_security_value",
			"kinara_collateral_condition",
			"kinara_description",
			"kinara_manufacturer_name",
			"kinara_model_number",
			"kinara_serial_number",
			"kinara_cersai_charge_required"
		]
		collateral_doc = frappe.db.get_value("Loan Security", collateral_id, collateral_fields, as_dict=True)
		sub_res.update(collateral_doc)

		sub_res.update({"allocated_loans": []})
		for loan in lsa_doc.allocated_loans:
			sub_res.allocated_loans.append({
				"loan": loan.loan,
			})

		res.append(sub_res)

	return res


@frappe.whitelist()
def release_collateral_against_loan(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)

	loan_security_release = frappe.new_doc("Loan Security Release")
	loan_security_release.loan = args.loan

	loan_security_release.append("securities", {
		"loan_security": args.collateral_id,
		"qty": 1,
	})

	loan_security_release.insert()
	loan_security_release.submit()

	return loan_security_release


@frappe.whitelist()
def release_collateral_against_customer(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)

	all_loans_and_lsa = frappe.db.sql(
		"""
		SELECT lsa.name as lsa
		FROM `tabLoan Security Assignment` lsa, `tabPledge` p, `tabLoan Security Assignment Loan Detail` lsald
		WHERE p.loan_security = %s
		AND p.parent = lsa.name
		AND lsald.parent = lsa.name
		AND lsa.status = 'Release Requested'
		""",
		(args.collateral_id),
		as_dict=True,
	)

	for d in all_loans_and_lsa or []:
		release_loan_security_assignment(d.lsa)


@frappe.whitelist()
def get_all_addresses_and_contacts_for_customer(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)

	addresses_and_contacts = {}

	addresses = frappe.db.get_all("Dynamic Link", filters={"parenttype": "Address", "link_doctype": "Customer", "link_name": args.customer}, pluck="parent")
	contacts = frappe.db.get_all("Dynamic Link", filters={"parenttype": "Contact", "link_doctype": "Customer", "link_name": args.customer}, pluck="parent")

	addresses_and_contacts['addresses'] = addresses
	addresses_and_contacts['contacts'] = contacts

	return addresses_and_contacts


@frappe.whitelist()
def update_contact(args):
	if isinstance(args, str):
		args = json.loads(args)

	args = frappe._dict(args)

	contact = frappe.get_doc("Contact", args.contact)

	if not contact:
		return

	old_email_id_row = frappe.db.get_value("Contact Email", {"parent": args.contact, "email_id": contact.email_id})
	if old_email_id_row and args.email_id:
		frappe.db.set_value("Contact Email", old_email_id_row, "email_id", args.email_id)
	elif args.email_id:
		contact.append("email_ids", {"email_id": args.email_id, "is_primary": 1})
		contact.save(ignore_permissions=True)
	elif "email_id" in args and not args.email_id:
		frappe.db.delete("Contact Email", {"parent": args.contact})
		contact.email_ids = []
		contact.save(ignore_permissions=True)

	old_mobile_no_row = frappe.db.get_value("Contact Phone", {"parent": args.contact, "phone": contact.mobile_no})
	if old_mobile_no_row and args.mobile_no:
		frappe.db.set_value("Contact Phone", old_mobile_no_row, "phone", args.mobile_no)
	elif args.mobile_no:
		contact.append("phone_nos", {"phone": args.mobile_no, "is_primary_mobile_no": 1})
		contact.save(ignore_permissions=True)
		for customer in frappe.db.get_all("Dynamic Link", filters={"parenttype": "Contact", "link_doctype": "Customer", "parent": args.contact}, pluck="link_name"):
			frappe.db.set_value("Customer", customer, "mobile_no", args.mobile_no)
	elif "mobile_no" in args and not args.mobile_no:
		frappe.db.delete("Contact Phone", {"parent": args.contact})
		contact.phone_nos = []
		contact.save(ignore_permissions=True)
		for customer in frappe.db.get_all("Dynamic Link", filters={"parenttype": "Contact", "link_doctype": "Customer", "parent": args.contact}, pluck="link_name"):
			frappe.db.set_value("Customer", customer, "mobile_no", "")

	contact.reload()

	contact.set_primary_email()
	contact.set_primary("mobile_no")

	contact.save(ignore_permissions=True)

	return {"email_id": args.email_id, "mobile_no": args.mobile_no}
