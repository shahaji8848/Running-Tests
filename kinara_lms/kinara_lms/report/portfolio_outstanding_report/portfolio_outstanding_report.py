# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import flt
from datetime import datetime
from frappe.utils import add_days, add_months, cint, date_diff, flt, get_last_day, getdate

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": ("Partner Name"),
			"fieldname": "partner_name",
			"fieldtype": "Link",
			"options": "Loan Partner",
			"width": 100
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
			"fieldtype": "Link",
			"options": "Branch",
			"width": 100
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
			"label": ("Applicant Occupation"),
			"fieldname": "applicant_occupation",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Business Sector"),
			"fieldname": "business_sector",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Last Instalment Date"),
			"fieldname": "maturity_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Customer Status"),
			"fieldname": "customer_status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("District"),
			"fieldname": "district",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Entity Name"),
			"fieldname": "entity_name",
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
			"label": ("Applicant Gender"),
			"fieldname": "applicant_gender",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Origination Source"),
			"fieldname": "origination_source",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Origination Source Name"),
			"fieldname": "origination_source_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Account ID"),
			"fieldname": "account_id",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Client ID"),
			"fieldname": "client_id",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Loan Product Cycle"),
			"fieldname": "loan_product_cycle",
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
			"label": ("Loan Officer Name"),
			"fieldname": "loan_officer_name",
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
			"label": ("Loan Disbursement Date"),
			"fieldname": "tranche_disbursement_date",
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
			"label": ("Interest Rate PCT"),
			"fieldname": "interest_rate_pct",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Processing Fee PCT"),
			"fieldname": "processing_fee_pct",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Processing Fee Amount"),
			"fieldname": "processing_fee_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Processing Fee Tax"),
			"fieldname": "gst_on_processing_fee_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Portfolio Insurance"),
			"fieldname": "portfolio_insurance_premium",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Commercial Cibil Charge"),
			"fieldname": "commercial_cibil_charge",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Security EMI"),
			"fieldname": "security_emi",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("BPI Duration Days"),
			"fieldname": "bpi_duration_days",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("BPI Amount"),
			"fieldname": "bpi_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Tenure Months"),
			"fieldname": "tenure_months",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("EMI Start Date"),
			"fieldname": "emi_start_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("First Disbursement Date"),
			"fieldname": "tranche_disbursement_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("EMI Date"),
			"fieldname": "emi_date",
			"fieldtype": "data",
			"width": 100
		},
		{
			"label": ("EMI Amount"),
			"fieldname": "emi_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Disbursement Month"),
			"fieldname": "disbursement_month",
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
			"label": ("Account Closed Date"),
			"fieldname": "account_closed_date",
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
			"label": ("Loan Sub Purpose"),
			"fieldname": "loan_sub_purpose",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Business Type"),
			"fieldname": "business_type",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Business Activity"),
			"fieldname": "business_activity",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Sector"),
			"fieldname": "sector",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Sub Sector"),
			"fieldname": "sub_sector",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("New Tenure"),
			"fieldname": "new_tenure",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("New Maturity Date"),
			"fieldname": "new_maturity_date",
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

	if filters.get("partner_name"):
		query_filters.update({"co_lending_partner": filters.get("partner_name")})
	query_filters.update({"docstatus": 1})
	
	loans = frappe.get_all(
		"Loan",
		filters=query_filters,
		fields=[
			"custom_hub_1",
			"custom_parent_branch",
			"loan_officer",
			"custom_loan_officer_name",
			"co_lending_partner",
			"applicant",
			"custom_individual_applicant",
			"custom_origination_source",
			"custom_origination_source_name",
			"name",
			"loan_product",
			"rate_of_interest",
			"repayment_periods",
			"repayment_start_date",
			"disbursement_date",
			"loan_purpose",
			"loan_sub_purpose",
			"custom_sector",
			"custom_sub_sector",
			"loan_amount",
			"total_payment",
			"total_principal_paid",
			"total_interest_payable",
			"written_off_amount",
			"custom_account_closed_date"
		],
	)
	
	for loan in loans:
		loan_count = frappe.db.sql("""select count(name) as total from `tabLoan` where applicant=%s and status in ('Disbursed','Partially Disbursed','Active')""",(loan.applicant),as_dict=True)
		if loan_count:
			if loan_count[0].get('total') > 1:
				customer_status = "Existing"
			else:
				customer_status = "New"

		gender =  frappe.db.get_value('Customer',loan.custom_individual_applicant,'gender')
		if gender:
			gender_value = frappe.db.get_value('Gender',gender,'value')
		else:
			gender_value = ''

		branch = get_hub_details(loan.custom_hub_1)
		loan_product = get_product_details(loan.loan_product)
		maturity_date = get_repayment_details(loan.name)

		applicant_name= frappe.db.get_value('Customer',loan.custom_individual_applicant,['customer_name'])
		contact = get_contact_details(applicant_name)
		if contact[0] != None:
			phone1 = contact[0]
		else:
			phone1 = ''
		if contact[1] != None:
			phone2 = contact[1]
		else:
			phone2 = ''
		
		entity_name= frappe.db.get_value('Customer',loan.applicant,['customer_name'])
		contact = get_contact_details(entity_name)
		if contact[0] != None:
			enphone1 = contact[0]
		else:
			enphone1 = ''
		if contact[1] != None:
			enphone2 = contact[1]
		else:
			enphone2 = ''

		count_disbusement = frappe.db.sql("""select count(name) as total from `tabLoan Disbursement` where against_loan=%s and docstatus = 1""",(loan.name),as_dict=True)
		if count_disbusement:
			count_disbus = count_disbusement[0].get('total')
		else:
			count_disbus = ''
		
		loan_disbusement =  frappe.db.sql("""select 
			sanctioned_loan_amount,
			disbursement_date,
			current_disbursed_amount,
			broken_period_interest,
			monthly_repayment_amount
			from `tabLoan Disbursement` where against_loan=%s and docstatus = 1 order by creation desc limit 1""",(loan.name),as_dict=True)
		if loan_disbusement:
			sanctioned_loan_amount = loan_disbusement[0].get('sanctioned_loan_amount')
			disbursement_date = loan_disbusement[0].get('disbursement_date')
			current_disbursed_amount = loan_disbusement[0].get('current_disbursed_amount')
			bpi_amt = loan_disbusement[0].get('broken_period_interest')
			monthly_repayment_amount = loan_disbusement[0].get('monthly_repayment_amount')
		else:
			sanctioned_loan_amount = ''
			disbursement_date = ''
			current_disbursed_amount = ''
			bpi_amt = ''
			monthly_repayment_amount = ''

		if loan.repayment_start_date:
			formatted_date = datetime.strptime(str(loan.repayment_start_date),"%Y-%m-%d")
			day = formatted_date.day
		else:
			day = ''

		if loan.disbursement_date:
			formatted_date1 = datetime.strptime(str(loan.disbursement_date), "%Y-%m-%d")
			formatted_string = formatted_date1.strftime("%B-%Y")
			month = formatted_string
		else:
			month = ''

		loan_repayment = frappe.db.sql("""select posting_date,repayment_start_date from `tabLoan Repayment Schedule` where loan=%s and status = "Active" order by creation desc limit 1""",(loan.name),as_dict=True)
		if loan_repayment:
			broken_period_interest_days = date_diff(add_months(loan_repayment[0].get('repayment_start_date'), -1), loan_repayment[0].get('posting_date'))
		else:
			broken_period_interest_days = ''

		row = {
			"zone": branch.get("zone_name"),
			"state": branch.get("state"),
			"division": branch.get("division"),
			"region": branch.get("region_name"),
			"hub_code": branch.get("name"),
			"hub_name": branch.get("hub_name"),
			"parent_branch": loan.custom_parent_branch,
			"loan_officer_name": loan.custom_loan_officer_name,
			"district": loan.region_name,
			"partner_name": loan.co_lending_partner,
			"customer_status": customer_status,
			"applicant_gender": gender_value,
			"entity_name": frappe.db.get_value('Customer',loan.applicant,'customer_name'), 
			"applicant_name": frappe.db.get_value('Customer',loan.custom_individual_applicant,'customer_name'),
			"origination_source": loan.custom_origination_source,
			"origination_source_name": loan.custom_origination_source_name,
			"account_id": loan.name,
			"client_id": loan.custom_individual_applicant,
			"loan_product_cycle": loan_product.get("cyclic_day_of_the_month"),
			"product_name": loan_product.get("product_name"),
			"loan_amount": loan.loan_amount,
			"principal_outstanding": flt(loan.get('total_payment'))- flt(loan.get('total_principal_paid'))- flt(loan.get('total_interest_payable'))- flt(loan.get('written_off_amount')),
			"tranche_number": count_disbus,
			"total_sanction_amount": sanctioned_loan_amount,
			"tranche_disbursement_date": disbursement_date,
			"tranche_disbursed_amount": current_disbursed_amount,
			"interest_rate_pct": loan.rate_of_interest,
			"bpi_amount": bpi_amt,
			"bpi_duration_days":broken_period_interest_days,
			"tenure_months": loan.repayment_periods,
			"emi_date": day,
			"emi_amount": monthly_repayment_amount,
			"disbursement_month": month,
			"emi_start_date": loan.repayment_start_date,
			"maturity_date": maturity_date,
			"loan_purpose": loan.loan_purpose,
			"loan_sub_purpose": loan.loan_sub_purpose,
			"business_type":  frappe.db.get_value('Customer',loan.custom_individual_applicant,'customer_type'),
			"business_activity": '',
			"sector": loan.custom_sector,
			"sub_sector": loan.custom_sub_sector,
			"account_closed_date": loan.custom_account_closed_date
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
			"cyclic_day_of_the_month",
			"product_name"
		]
	)
	if loan_product:
		return loan_product[0]
	else:
		return {}

def get_repayment_details(loan):
	loan_repayment = frappe.db.get_value("Loan Repayment Schedule",{"loan":loan},"name")
	if loan_repayment != None:
		values = {'parent': loan_repayment}
		data = frappe.db.sql("""select max(idx) as idx from `tabRepayment Schedule` where parent =  %(parent)s""", values=values, as_dict=1)
		loan_repayment = frappe.db.get_value("Repayment Schedule",{"parent":loan_repayment, "idx":data[0].get("idx")},"payment_date")
		return loan_repayment

def get_contact_details(customer):
	parent = frappe.db.get_value('Dynamic Link',{'link_title': customer},'parent')
	phone1 = frappe.db.get_value('Contact Phone',{'parent': parent,'idx':1},'phone')
	phone2 = frappe.db.get_value('Contact Phone',{'parent': parent,'idx':2},'phone')
	return phone1,phone2
	