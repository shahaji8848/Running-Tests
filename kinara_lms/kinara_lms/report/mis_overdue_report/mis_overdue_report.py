# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from kinara_lms.apis.loan_more_response import repayment_schedule_details


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": ("Report Date"),
			"fieldname": "report_date",
			"fieldtype": "Date",
			"width": 120
		},
		{
			"label": ("Zone"),
			"fieldname": "zone",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("State"),
			"fieldname": "state",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Division"),
			"fieldname": "division",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Region"),
			"fieldname": "region",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Parent Branch"),
			"fieldname": "parent_branch",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": ("Hub Code"),
			"fieldname": "hub_code",
			"fieldtype": "Link",
			"options": "Branch",
			"width": 100
		},
		{
			"label": ("Hub Name"),
			"fieldname": "hub_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Client ID"),
			"fieldname": "client_id",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 100
		},
		{
			"label": ("Enterprise Name"),
			"fieldname": "enterprise_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Account Number"),
			"fieldname": "account_number",
			"fieldtype": "Link",
			"options": "Loan",
			"width": 100
		},
		{
			"label": ("Loan Product Cycle"),
			"fieldname": "loan_product_cycle",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Applicant Name"),
			"fieldname": "applicant_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Loan Officer Name"),
			"fieldname": "loan_officer_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Product Name"),
			"fieldname": "product_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Tenure"),
			"fieldname": "tenure",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Frequency"),
			"fieldname": "frequency",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Loan Amount"),
			"fieldname": "loan_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Restructured Loan Amount"),
			"fieldname": "restructured_loan_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Disbursement Date"),
			"fieldname": "disbursement_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("EMI"),
			"fieldname": "emi",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Installment Start Date"),
			"fieldname": "installment_start_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Maturity Date"),
			"fieldname": "maturity_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Loan Purpose"),
			"fieldname": "loan_purpose",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Balance Term"),
			"fieldname": "balance_term",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Term Till Date"),
			"fieldname": "term_till_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Principal Outstanding"),
			"fieldname": "principal_outstanding",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Principal Overdue"),
			"fieldname": "principal_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Interest Overdue"),
			"fieldname": "interest_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Addition Interest Overdue"),
			"fieldname": "addition_interest_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Penal Interest Overdue"),
			"fieldname": "penal_interest_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Booked Penal Interest"),
			"fieldname": "booked_penal_interest",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("CBC Overdue"),
			"fieldname": "cbc_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Other Charges Overdue"),
			"fieldname": "other_charges_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Security Deposit Due"),
			"fieldname": "security_deposit_due",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Total Overdue"),
			"fieldname": "total_overdue",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Overdue Days"),
			"fieldname": "overdue_days",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("DPD Bucket"),
			"fieldname": "dpd_bucket",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("NPA"),
			"fieldname": "npa",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Last Repayment Date"),
			"fieldname": "last_repayment_date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": ("Last Repayment Amount"),
			"fieldname": "last_repayment_amount",
			"fieldtype": "Currency",
			"options": "currency",
			"width": 100
		},
		{
			"label": ("Last Repayment Mode"),
			"fieldname": "last_repayment_mode",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("No Of EMI Overdue"),
			"fieldname": "no_of_emi_overdue",
			"fieldtype": "Data",
			"width": 100
		}
	]
	return columns

def get_data(filters):
	data = []
	query_filters = {
		"posting_date": filters.get("date"),
	}

	if filters.get("hub"):
		query_filters.update({"custom_hub_1": filters.get("hub")})
	
	loans = frappe.get_all(
		"Loan",
		filters=query_filters,
		fields=[
			"loan_account_number",
			"custom_hub_1",
			"applicant",
			"loan_officer",
			"loan_product",
			"repayment_periods",
			"repayment_frequency",
			"loan_amount",
			"disbursement_date",
			"custom_individual_applicant",
			"repayment_start_date",
			"loan_purpose",
			"total_payment",
			"status",
			"disbursed_amount",
			"total_principal_paid",
			"total_interest_payable",
			"written_off_amount",
			"days_past_due",
			"classification_code",
			"is_npa",
			"manual_npa",
			"custom_parent_branch"

		],
	)

	for loan in loans:
		if not filters.get("hub"):
			branch = get_hub_details(loan.custom_hub_1)
		else:
			branch = get_hub_details(filters.get("hub"))
		loan_product = get_product_details(loan.loan_product)
		loan_disb = get_disbursement_details(loan.loan_account_number)
		loan_restruc = get_restructure_details(loan.loan_account_number)
		loan_repayment = get_repayment_details(loan.loan_account_number)
		total_payment = loan.total_payment if loan.status == "Disbursed" else loan.disbursed_amount

		pio = frappe.db.sql("""select outstanding_amount from `tabLoan Demand` where loan=%s and demand_type = "Penalty" and demand_subtype = "Penalty" order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if pio:
			penal_interest_overdue = pio[0].get('outstanding_amount')
		else:
			penal_interest_overdue = ''

		bpi = frappe.db.get_value("Loan Interest Accrual",{"loan":loan.loan_account_number},"interest_amount")
		if bpi:
			booked_penal_interest = bpi
		else:
			booked_penal_interest = ''

		cbc = frappe.db.sql("""select outstanding_amount from `tabLoan Demand` where loan=%s and demand_type = "Charges" and demand_subtype = "Charges" order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if cbc:
			cbc_overdue = cbc[0].get('outstanding_amount')
		else:
			cbc_overdue = ''

		other_charges = frappe.db.sql("""select outstanding_amount from `tabLoan Demand` where loan=%s and demand_type = "Other Charges" and demand_subtype = "Other Charges" order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if other_charges:
			other_charges_overdue = other_charges[0].get('outstanding_amount')
		else:
			other_charges_overdue = ''

		if (loan.is_npa or loan.manual_npa) == 1:
			npa = "NPA"
		else:
			npa = "NORMAL"

		balance_term = ''
		term_till_date = ''
		loan_repayment = frappe.db.sql("""select name from `tabLoan Repayment Schedule` where loan=%s and status = "Active" order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if loan_repayment:
			loan_repayment_name = loan_repayment[0].get('name')
			
			repayment_schedule_demand_checked = frappe.db.sql("""select name from `tabRepayment Schedule` where parent=%s and demand_generated = 0""",(loan_repayment_name),as_dict=True)
			balance_term = len([ele for ele in repayment_schedule_demand_checked])
			
			repayment_schedule_demand_unchecked = frappe.db.sql("""select name from `tabRepayment Schedule` where parent=%s and demand_generated = 1""",(loan_repayment_name),as_dict=True)
			term_till_date = len([ele for ele in repayment_schedule_demand_unchecked])

		repayment = frappe.db.sql("""select posting_date,amount_paid from `tabLoan Repayment` where against_loan=%s order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if repayment:
			last_repayment_date = repayment[0].get("posting_date")
			last_repayment_amount = repayment[0].get("amount_paid")
		else:
			last_repayment_date = ''
			last_repayment_amount = ''

		principal_overdue = frappe.db.sql("""select demand_amount,paid_amount from `tabLoan Demand` where loan=%s and demand_type = "EMI" and demand_subtype = "Principal" order by creation desc limit 1""",(loan.loan_account_number),as_dict=True)
		if principal_overdue:
			principal_overdue_amount = principal_overdue[0].get('demand_amount') - principal_overdue[0].get('paid_amount')
		else:
			principal_overdue_amount = ''

		total_overdue = flt(penal_interest_overdue) + flt(cbc_overdue) + flt(other_charges_overdue)
		if total_overdue == None or '':
			total_overdue = 0

		noofEMIsOverdue = ''
		repayment_schedule = repayment_schedule_details(loan.loan_account_number)
		if repayment_schedule:
			noofEMIsOverdue = repayment_schedule.get('idx') - repayment_schedule.get('emi_paid')
		
		row = {
			"report_date": filters.get("date"),
			"zone": branch.get("zone_name"),
			"state": branch.get("state"),
			"division": branch.get("division"),
			"region": branch.get("region_name"),
			"parent_branch": '',
			"hub_code": branch.get("name"),
			"hub_name": branch.get("hub_name"),
			"client_id": loan.custom_individual_applicant,
			"enterprise_name": frappe.db.get_value('Customer',loan.applicant,'customer_name'), 
			"account_number": loan.loan_account_number,
			"loan_product_cycle": loan_product.get("cyclic_day_of_the_month"),
			"applicant_name": frappe.db.get_value('Customer',loan.custom_individual_applicant,'customer_name'),
			"loan_officer_name": loan.loan_officer,
			"product_name": loan.loan_product,
			"tenure": loan.repayment_periods,
			"frequency": loan.repayment_frequency,
			"loan_amount": loan.loan_amount,
			"restructured_loan_amount": loan_restruc.get("new_loan_amount"),
			"disbursement_date": loan_disb.get("disbursement_date"),
			"emi": loan_disb.get("monthly_repayment_amount"),
			"installment_start_date": loan.repayment_start_date,
			"maturity_date": loan_repayment,
			"loan_purpose": loan.loan_purpose,
			"principal_outstanding": flt(total_payment)
				- flt(loan.total_principal_paid)
				- flt(loan.total_interest_payable)
				- flt(loan.written_off_amount),
			"penal_interest_overdue" : penal_interest_overdue,
			"booked_penal_interest": booked_penal_interest,
			"cbc_overdue": cbc_overdue,
			"other_charges_overdue": other_charges_overdue,
			"overdue_days": loan.days_past_due,
			"dpd_bucket": loan.classification_code,
			"npa": npa,
			"parent_branch": loan.custom_parent_branch,
			"balance_term": balance_term,
			"term_till_date": term_till_date,
			"last_repayment_date": last_repayment_date,
			"last_repayment_amount": last_repayment_amount,
			"principal_overdue": principal_overdue_amount,
			"total_overdue": total_overdue,
			"no_of_emi_overdue": noofEMIsOverdue
		}
		data.append(row)
	return data

def get_hub_details(hub):
	hub = frappe.get_all(
		"Branch",
		filters={'name':hub},
		fields=[
			"zone_name",
			"state",
			"division",
			"region_name",
			"name",
			"hub_name"
		]
	)
	if hub:
		return hub[0]
	else:
		return {}

def get_product_details(loan):
	loan_product = frappe.get_all(
		"Loan Product",
		filters={'name':loan},
		fields=[
			"cyclic_day_of_the_month"
		]
	)
	if loan_product:
		return loan_product[0]
	else:
		return {}

def get_disbursement_details(loan):
	loan_disb = frappe.get_all(
		"Loan Disbursement",
		filters={'against_loan':loan},
		fields=[
			"disbursement_date",
			"monthly_repayment_amount"
		]
	)
	if loan_disb:
		return loan_disb[0]
	else:
		return {}

def get_restructure_details(loan):
	loan_restruc = frappe.get_all(
		"Loan Restructure",
		filters={'loan':loan},
		fields=[
			"new_loan_amount"
		]
	)
	if loan_restruc:
		return loan_restruc[0]
	else:
		return {}

def get_repayment_details(loan):
	loan_repayment = frappe.db.get_value("Loan Repayment Schedule",{"loan":loan},"name")
	if loan_repayment != None:
		values = {'parent': loan_repayment}
		data = frappe.db.sql("""select max(idx) as idx from `tabRepayment Schedule` where parent =  %(parent)s""", values=values, as_dict=1)
		loan_repayment = frappe.db.get_value("Repayment Schedule",{"parent":loan_repayment, "idx":data[0].get("idx")},"payment_date")
		return loan_repayment
