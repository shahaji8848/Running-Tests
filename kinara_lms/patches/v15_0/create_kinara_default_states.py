from frappe.desk.page.setup_wizard.setup_wizard import make_records

from kinara_lms.constants.kinara_default_states import KINARA_DEFAULT_STATES


def execute():
	make_records(KINARA_DEFAULT_STATES)
