# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt


import frappe
import datetime
from frappe.model.document import Document

class BillofSupply(Document):
    def before_save(self):
        total = 0
        for item in self.items:
            total += item.amount
        self.append('items',{'particulars':"Total Amount",'amount':total})