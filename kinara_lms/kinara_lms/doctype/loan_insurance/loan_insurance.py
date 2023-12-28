# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoanInsurance(Document):
	def before_save(self):
		if self.nominee_urn:
			customer = frappe.get_doc("Customer", self.nominee_urn)
			self.nominee_name = customer.customer_name
