import json

import frappe


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
	
	charge.insert(ignore_permissions=True)

	return charge
