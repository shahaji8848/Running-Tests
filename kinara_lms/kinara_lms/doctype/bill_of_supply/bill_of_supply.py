# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt


import frappe
import datetime
from frappe.model.document import Document
from frappe.utils.data import flt


class BillofSupply(Document):
    def before_save(self):
        self.posting_date = datetime.datetime.now().date()
        if self.demand_type == "EMI":
            self.customer_address = frappe.db.get_value('Customer', self.customer_urn, 'customer_primary_address')
            if not self.customer_address:
                customer_address = self.get_primary_details("Customer",self.customer_urn)
                if len(customer_address) > 0:
                    self.customer_address = customer_address[0][0]
                    self.customer_gstin = customer_address[0][1]
            else:
                self.customer_gstin = frappe.db.get_value('Address', self.customer_address, 'gstin')
            company_name = frappe.db.get_value('Loan', self.loan_id, 'company')
            company_details = self.get_primary_details("Company",company_name)
            if len(company_details) > 0:
                self.company_address = company_details[0][0]
                self.company_gstin = company_details[0][1]
                self.company_state_code = company_details[0][2]
                company_city = company_details[0][3] + ", " if company_details[0][3] else ""
                company_state = company_details[0][4] if company_details[0][4] else ""
                gst_state = company_details[0][5] if company_details[0][5] else ""
                self.place_of_supply = company_city + (company_state or gst_state)
                self.repayment_schedule_detail = self.repayment_schedule_detail
        if self.demand_type == "Charges":
            if self.company_address:
                company_city, company_state, gst_state = frappe.db.get_value("Address", self.company_address, ['city', 'state', 'gst_state'])
                company_city = company_city + ", " if company_city else ""
                company_state = company_state if company_state else ""
                gst_state = gst_state if gst_state else ""
                self.place_of_supply = company_city + (company_state or gst_state)
        total = 0
        for item in self.items:
            total += flt(item.amount)
        self.append('items',{'particulars':"Total Amount",'amount':total})   

    def get_primary_details(*args):
        conditions = f"""WHERE dl.parenttype = "Address" 
                    AND dl.parentfield = "links" 
                    AND dl.link_doctype = "{args[1]}" 
                    AND dl.link_name = "{args[2]}" 
                    AND ads.is_primary_address = 1"""""
        result = frappe.db.sql(f"""SELECT ads.name, ads.gstin, ads.gst_state_number, ads.city, ads.state, ads.gst_state
                                FROM `tabAddress` as ads
                                JOIN `tabDynamic Link` as dl
                                ON ads.name = dl.parent
                                {conditions}
                                LIMIT 1""")
        return result