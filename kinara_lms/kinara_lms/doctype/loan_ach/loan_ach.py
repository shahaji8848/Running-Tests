# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoanACH(Document):
	def validate(self):
		if self.thirty_year_end == 1:
			if self.ach_start_date is not None:
				self.ach_end_date = frappe.utils.data.add_years(self.ach_start_date, 30)
			else:
				frappe.throw("Invalid ACH Start Date")
	
	def before_save(self):
		umrn_no = frappe.db.get_value('Loan ACH', self.name, 'umrn_no')
		if self.umrn_no != umrn_no:
			self.processed_on_with_umrn = frappe.utils.nowdate()
		if not self.umrn_no:
			self.processed_on_with_umrn = None