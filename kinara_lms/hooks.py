app_name = "kinara_lms"
app_title = "Kinara LMS"
app_publisher = "Visage Holdings and Finance Private Limited)"
app_description = "LMS for Kinara Capital"
app_email = "help@kinaracapital.com"
app_license = "MIT"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/kinara_lms/css/kinara_lms.css"
# app_include_js = "/assets/kinara_lms/js/kinara_lms.js"

# include js, css files in header of web template
# web_include_css = "/assets/kinara_lms/css/kinara_lms.css"
# web_include_js = "/assets/kinara_lms/js/kinara_lms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "kinara_lms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
	"Loan Partner": "public/js/lending/loan_partner.js",
	"Loan": "public/js/lending/loan.js",
	"Company":  "public/js/erpnext/company.js",
	"Loan Disbursement":  "public/js/erpnext/loan_disbursement.js",
	"Address":  "public/js/erpnext/address.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "kinara_lms.utils.jinja_methods",
#	"filters": "kinara_lms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "kinara_lms.install.before_install"
after_install = "kinara_lms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "kinara_lms.uninstall.before_uninstall"
# after_uninstall = "kinara_lms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "kinara_lms.utils.before_app_install"
# after_app_install = "kinara_lms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "kinara_lms.utils.before_app_uninstall"
# after_app_uninstall = "kinara_lms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "kinara_lms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

override_doctype_class = {
	"Customer": "kinara_lms.overrides.customer_master.CustomerMaster",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Loan Product": {
		"validate": "kinara_lms.overrides.loan_product.validate_loan_product_code",
	},
	"Address": {
		"before_validate": "kinara_lms.overrides.address.before_validate",
		"validate": "kinara_lms.overrides.address.kinara_address_validate",
	},
	"Contact": {
		"validate": "kinara_lms.overrides.contact.validate_contact",
	},
	"Loan": {
		"after_insert": "kinara_lms.overrides.loan.created_loan_related_docs",
		"autoname": "kinara_lms.overrides.loan.override_name",
		"validate": "kinara_lms.overrides.loan.validate_customer_type",
	},
	"Loan Partner": {
		"validate": "kinara_lms.overrides.loan_partner.validate_loan_partner",
	},
	"Sales Invoice": {
		"on_update": "kinara_lms.overrides.sales_invoice.on_update",
        "on_submit": "kinara_lms.overrides.sales_invoice.on_submit",
	},
	"Company":{
		"validate": "kinara_lms.overrides.company.validate_default_disbursement_account",
	},
    "Loan Demand":{
		"on_submit": "kinara_lms.overrides.loan_demand.on_submit",
	},
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"kinara_lms.tasks.all"
#	],
#	"daily": [
#		"kinara_lms.tasks.daily"
#	],
#	"hourly": [
#		"kinara_lms.tasks.hourly"
#	],
#	"weekly": [
#		"kinara_lms.tasks.weekly"
#	],
#	"monthly": [
#		"kinara_lms.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "kinara_lms.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "kinara_lms.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "kinara_lms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["kinara_lms.utils.before_request"]
# after_request = ["kinara_lms.utils.after_request"]

# Job Events
# ----------
# before_job = ["kinara_lms.utils.before_job"]
# after_job = ["kinara_lms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"kinara_lms.auth.validate"
# ]
fixtures = [
	{"dt": "Custom Field", "filters": [
		[
			"name", "in", [
				"Bank Account Type-custom_type_id",
				"Bank Account Type-custom_value",
				"Bank Account Type-custom_category_type",
				"Bank Account Type-custom_disabled",
				"Salutation-custom_type_id",
				"Salutation-custom_value",
				"Salutation-custom_category_type",
				"Salutation-custom_disabled",
				"Gender-custom_type_id",
				"Gender-custom_value",
				"Gender-custom_category_type",
				"Gender-custom_disabled",
				"Branch-custom_hub_code",
				"Branch-custom_zone_name",
				"Branch-custom_region_name",
				"Branch-custom_hub_name",
				"Branch-custom_zone_code",
				"Branch-custom_division",
				"Branch-custom_location_code",
				"Branch-custom_hub_address_line_2",
				"Branch-custom_hub_address_line_3",
				"Branch-custom_state_code",
				"Branch-custom_hub_address_line_1",
				"Branch-custom_division_code",
				"Branch-custom_hub_id",
				"Branch-custom_region_code",
				"Branch-custom_state",
				"Branch-custom_disabled",
				"Branch-custom_column_break_gzacv",
				"Bank-custom_bank_id",
				"Bank-custom_disabled",
				"Loan Security Type-custom_collateral_type_id",
				"Loan Security Type-custom_collateral_type",
				"Loan Product-custom_base_rate",
				"Loan Product-custom_write_off__knockoff_sequence",
				"Loan Product-custom_npa_knockoff_sequence",
				"Loan Product-custom_standard_knockoff_sequence",
				"Loan Product-custom_dpd_threshold_for_sub_standard_definition",
				"Loan Product-custom_sub_standard_definition_for_collection_offset_logic",
				"Loan Product-custom_mutitranche_allowed",
				"Loan Product-custom_interest_treatment_after_moratorium_period",
				"Loan Product-custom_minimum_days_for_1st_repayment_date",
				"Loan Product-custom_foreclosure_allowed",
				"Loan Product-custom_part_prepayment_allowed",
				"Loan Product-custom_partial_payment_allowed",
				"Loan Product-custom_advance_payment_allowed",
				"Loan Product-custom_day_count_convention",
				"Loan Product-custom_repayment_demand_frequency",
				"Loan Product-custom_repayment_method",
				"Loan Product-custom_default_tenure",
				"Loan Product-custom_maximum_tenure",
				"Loan Product-custom_minimum_tenure",
				"Loan Product-custom_roi_type",
				"Loan Product-custom_minimum_loan_amount",
				"Loan Product-custom_default_loan_amount",
				"Loan Product-custom_minimum_spread_rate",
				"Loan Product-custom_maximum_spread_rate",
				"Loan Security Type-custom_type_id",
				"Loan Adjustment-custom_foreclosure_charges",
				"Loan Adjustment-custom_mode_of_payment",
				"Loan Adjustment-custom_payment_gateway",
				"Loan Partner-custom_disbursement_details",
				"Loan Partner-custom_partner_cin",
				"Loan Partner-custom_partner_rbi",
				"Loan Partner-custom_partner_full_name",
				"Loan Partner-custom_ifsc_code_collections",
				"Loan Partner-custom_escrow_applicable_flag_collections",
				"Loan Partner-custom_bank_name_disbursement",
				"Loan Partner-custom_ifsc_code_disbursement",
				"Loan Partner-custom_escrow_applicable_flag_disbursement",
				"Loan Partner-custom_collections_details",
				"Loan Partner-custom_bank_account_number_disbursement",
				"Loan Partner-custom_column_break_xsx3x",
				"Loan Partner-custom_column_break_xt3gw",
				"Loan Partner-custom_bank_name_collections",
				"Loan Partner-custom_bank_account_number_collections",
				"Company-custom_default_disbursement_account",
				"Company-custom_gst_regime",
			]
		]
	]},
	{"dt": "Property Setter", "filters": [
		[
			"name", "in", [
				"Customer-customer_type-options",
				"Bank Account Type-main-naming_rule",
				"Bank Account Type-main-autoname",
				"Bank Account Type-main-field_order",
				"Bank Account Type-account_type-hidden",
				"Salutation-main-field_order",
				"Salutation-salutation-hidden",
				"Salutation-main-naming_rule",
				"Salutation-main-autoname",
				"Gender-gender-hidden",
				"Gender-main-naming_rule",
				"Gender-main-autoname",
				"Gender-main-field_order",
				"Branch-main-naming_rule",
				"Branch-main-autoname",
				"Branch-main-field_order",
				"Bank-main-naming_rule",
				"Bank-main-autoname",
				"Bank-main-field_order",
				"Loan Security Type-main-field_order",
				"Loan Security Type-main-autoname",
				"Loan Security Type-main-naming_rule",
				"Loan Product-main-field_order",
				"Loan Product-loan_category-reqd",
				"Loan Security Deposit-main-field_order",
				"Loan Product-grace_period_in_days-reqd",
				"Loan Product-penalty_interest_method-reqd",
				"Loan Adjustment-is_foreclosure-hidden",
				"Loan Partner-main-field_order",
				"Company-main-field_order",
				"Loan Adjustment-main-field_order",
			]
		]
	]}
]
