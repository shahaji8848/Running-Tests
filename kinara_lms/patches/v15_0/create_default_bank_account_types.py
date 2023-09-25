from frappe.desk.page.setup_wizard.setup_wizard import make_records


def execute():
	records = [
		# Bank Account Types
		{"doctype": "Bank Account Type", "account_type": "Disbursement"},
		{"doctype": "Bank Account Type", "account_type": "Collections"},
		{"doctype": "Bank Account Type", "account_type": "Disbursement & Collections"},
	]

	make_records(records)
