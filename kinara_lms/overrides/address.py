import json

import frappe

from india_compliance.gst_india.overrides.party import update_docs_with_previous_gstin, get_docs_with_previous_gstin


def kinara_address_validate(doc, method=None):
	if doc.state:
		doc.state = frappe.db.get_value("Kinara State", doc.state, "system_state_name")
	
	if frappe.flags.in_update_docs_with_previous_gstin:
		return

	frappe.flags.in_update_docs_with_previous_gstin = True

	previous_gstin = (doc.get_doc_before_save() or {}).get("gstin")

	if not previous_gstin or previous_gstin == doc.gstin:
		return

	docs_with_previous_gstin = get_docs_with_previous_gstin(
		previous_gstin, doc.doctype, doc.name
    )

	if not docs_with_previous_gstin:
		return

	update_docs_with_previous_gstin(doc.gstin, doc.gst_category, json.dumps(docs_with_previous_gstin))


def before_validate(doc,method=None):
	set_state(doc)

def set_state(doc):
	if doc.geo_type_id:
		state = frappe.db.get_value('Geo', doc.geo_type_id, 'state')
		doc.state = state
