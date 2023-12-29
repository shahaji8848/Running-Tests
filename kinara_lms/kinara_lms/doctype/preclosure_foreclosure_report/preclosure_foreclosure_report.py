# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from lending.loan_management.doctype.loan_repayment.loan_repayment import calculate_amounts
from datetime import datetime


class PreclosureForeclosureReport(Document):
	def before_save(self):
		loan_id = frappe.get_value("Loan", filters={"name":self.loan_account_number}, fieldname=["name","applicant","branch"],as_dict=True)
		print(loan_id['applicant'])
		self.client_id = loan_id.get("applicant","")
		self.hub = loan_id.get("branch","")

		customer = frappe.get_value("Customer", filters={"name":loan_id['applicant']}, fieldname=["customer_name","customer_primary_address"],as_dict=True)
		address = customer.customer_primary_address
		if address:
			self.client_address = address

		self.client_name = customer['customer_name']
		self.printed_date = datetime.now()
		self.printed_by = frappe.session.user
		self.working_date = datetime.now().date()
		self.set('preclosure_foreclosure_table', [])
		set_childTbale_data(self)

def set_childTbale_data(self):
		childTable_data = calculate_amounts(self.loan_account_number, self.proposed_closure_date, "Loan Closure")
		
		totalPrincipalDue = childTable_data.get("payable_principal_amount",0)
		totalFuturePrincipal = childTable_data.get("total_future_principal",0)
		totalNormalInterestDue = childTable_data.get("interest_amount",0)
		totalPenalInterestDue = childTable_data.get("penalty_amount",0)
		totalFeeDue = childTable_data.get("total_charges_payable",0)

		totalDemandDue = childTable_data.get("payable_principal_account", 0)+childTable_data.get("interest_amount", 0)+childTable_data.get("penalty_amount", 0)+childTable_data.get("total_charges_payable"),

		interestAccruedNotDemanded = childTable_data.get("undue_interest",0)
		principalOutstanding = childTable_data.get("pending_principal_amount",0)
		totalOverdue = childTable_data.get("payable_amount",0)

		self.append('preclosure_foreclosure_table', {"component":"Total Principal Due","amount":totalPrincipalDue})
		self.append('preclosure_foreclosure_table', {"component":"Total Future Principal","amount":totalFuturePrincipal})
		self.append('preclosure_foreclosure_table', {"component":"Total Normal Interest Due","amount":totalNormalInterestDue})
		self.append('preclosure_foreclosure_table', {"component":"Total Penal Interest Due","amount":totalPenalInterestDue})
		self.append('preclosure_foreclosure_table', {"component":"Total Fee Due","amount":totalFeeDue})
		self.append('preclosure_foreclosure_table', {"component":"Total Demand Due","amount":totalDemandDue})
		self.append('preclosure_foreclosure_table', {"component":"Interest Accrued Not Demanded","amount":interestAccruedNotDemanded})
		self.append('preclosure_foreclosure_table', {"component":"Principal Outstanding","amount":principalOutstanding})
		self.append('preclosure_foreclosure_table', {"component":"Total Overdue","amount":totalOverdue})