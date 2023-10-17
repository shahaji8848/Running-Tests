from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.custom.doctype.property_setter.property_setter import make_property_setter

from kinara_lms.constants.kinara_default_states import KINARA_DEFAULT_STATES


KINARA_CUSTOM_FIELDS = {
	"Customer": [
		{
			"fieldname": "customer_urn",
			"label": "Customer URN",
			"fieldtype": "Data",
			"insert_after": "customer_name",
			"unique": 1,
			"reqd": 1,
		},
	],
	"Loan Partner": [
		{
			"fieldname": "processing_fee_billing",
			"label": "Processing Fee Billing (against partner share)",
			"fieldtype": "Percent",
			"insert_after": "servicer_fee",
		},
	],
	"Item": [
		{
			"default": "0",
			"fieldname": "tax_inclusive",
			"label": "Tax Inclusive",
			"fieldtype": "Check",
			"insert_after": "stock_uom",
		},
	],
	"Loan": [
		{
			"fieldname": "loan_id",
			"label": "Loan ID",
			"fieldtype": "Data",
			"unique": 1,
			"insert_after": "applicant"
		},
		{
			"fieldname": "loan_application_id",
			"label": "Loan Application ID",
			"fieldtype": "Data",
			"unique": 1,
			"insert_after": "loan_id"
		},
		{
			"fieldname": "loan_account_number",
			"label": "Loan Account Number",
			"fieldtype": "Data",
			"unique": 1,
			"insert_after": "loan_id"
		},
		{
			"fieldname": "loan_partner",
			"label": "Loan Partner",
			"fieldtype": "Link",
			"options": "Loan Partner",
			"insert_after": "company"
		},
		{
			"fieldname": "kinara_lms_details",
			"label": "Kinara LMS Details",
			"fieldtype": "Section Break",
			"insert_after": "is_term_loan",
			"collapsible": 1
		},
		{
			"fieldname": "hub",
			"label": "Hub",
			"fieldtype": "Data",
			"insert_after": "kinara_lms_details"
		},
		{
			"fieldname": "loan_officer",
			"label": "Loan Officer",
			"fieldtype": "Data",
			"insert_after": "hub"
		},
		{
			"default": 0,
			"fieldname": "her_vikas",
			"label": "Her Vikas",
			"fieldtype": "Check",
			"insert_after": "loan_officer"
		},
		{
			"fieldname": "channel",
			"label": "Channel",
			"fieldtype": "Data",
			"insert_after": "her_vikas"
		},
		{
			"fieldname": "lap_combo",
			"label": "LAP Combo",
			"fieldtype": "Check",
			"insert_after": "channel"
		},
		{
			"fieldname": "green_finance_flag",
			"label": "Green Finance Flag",
			"fieldtype": "Check",
			"insert_after": "lap_combo"
		},
		{
			"fieldname": "direct_assignment_tagging",
			"label": "Securitization/ Direct Assignment Tagging",
			"fieldtype": "Data",
			"insert_after": "green_finance_flag"
		},
		{
			"fieldname": "kinara_column_break",
			"fieldtype": "Column Break",
			"insert_after": "direct_assignment_tagging"
		},
		{
			"fieldname": "loan_purpose",
			"label": "Loan Purpose",
			"fieldtype": "Data",
			"insert_after": "kinara_column_break"
		},
		{
			"fieldname": "loan_sub_purpose",
			"label": "Loan Sub Purpose",
			"fieldtype": "Data",
			"insert_after": "loan_purpose"
		},
		{
			"fieldname": "effective_interest_rate",
			"label": "Annualized Percentage/Effective Interest Rate",
			"fieldtype": "Float",
			"insert_after": "green_finance_flag"
		},
	]
}


def after_install():
	create_custom_fields(KINARA_CUSTOM_FIELDS, ignore_validate=True)
	make_fixtures()
	add_property_setters()


def make_fixtures():
	records = [
		# Bank Account Types
		{"doctype": "Bank Account Type", "account_type": "Disbursement"},
		{"doctype": "Bank Account Type", "account_type": "Collections"},
		{"doctype": "Bank Account Type", "account_type": "Disbursement & Collections"},\
	] + KINARA_DEFAULT_STATES

	make_records(records)

def add_property_setters():
	make_property_setter(
		"Sales Invoice",
		"customer",
		"fetch_from",
		"loan.applicant",
		"Small Text",
		validate_fields_for_doctype=False,
	)
