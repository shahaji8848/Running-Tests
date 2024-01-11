# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt


import frappe
import datetime
from frappe.model.document import Document
from frappe.utils.data import flt


class BillofSupply(Document):
    def before_save(self):
        if self.customer_urn:
            self.customer = frappe.db.get_value('Customer', self.customer_urn, 'customer_name')
        if self.applicant_urn:
            self.applicant = frappe.db.get_value('Customer', self.applicant_urn, 'customer_name')
        total = 0
        for item in self.items:
            total += flt(item.amount)
        self.append('items',{'particulars':"Total Amount",'amount':total})