import frappe


def map_kinara_state_to_system_state(doc, method=None):
	if doc.state:
		doc.state = frappe.db.get_value("Kinara State", doc.state, "system_state_name")
