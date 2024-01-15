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
			"label": ("Loan Officer ID"),
			"fieldname": "loan_officer_id",
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
			"label": ("District"),
			"fieldname": "district",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Partner Name"),
			"fieldname": "partner_name",
			"fieldtype": "Link",
			"options": "Loan Partner",
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
			"label": ("Kinara Application Id"),
			"fieldname": "kinara_application_id",
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
			"label": ("Product Code"),
			"fieldname": "product_code",
			"fieldtype": "Link",
			"options": "Loan Product",
			"width": 100
		},
		{
			"label": ("Product Name"),
			"fieldname": "product_name",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Created By"),
			"fieldname": "created_by",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Tranche Number"),
			"fieldname": "tranche_number",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Total Sanction Amount"),
			"fieldname": "total_sanction_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Tranche Disbursement Date"),
			"fieldname": "tranche_disbursement_date",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Tranche Disbursed Amount"),
			"fieldname": "tranche_disbursed_amount",
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
			"label": ("GST On Processing Fee Amount"),
			"fieldname": "gst_on_processing_fee_amount",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Portfolio Insurance Premium"),
			"fieldname": "portfolio_insurance_premium",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Portfolio Insurance Service Charge"),
			"fieldname": "portfolio_insurance_service_charge",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Portfolio Insurance Service Tax On Service Charge"),
			"fieldname": "portfolio_insurance_service_tax_on_service_charge",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Documentation Charge"),
			"fieldname": "documentation_charge",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("GST On Documentation Charge"),
			"fieldname": "gst_on_documentation_charge",
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
			"label": ("LTV PCT"),
			"fieldname": "ltv_pct",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("IIR"),
			"fieldname": "iir",
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
			"label": ("EMI Start Date"),
			"fieldname": "emi_start_date",
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
			"label": ("Account Status"),
			"fieldname": "account_status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Applicant Mobile 1"),
			"fieldname": "applicant_mobile_1",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Applicant Mobile 2"),
			"fieldname": "applicant_mobile_2",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Co-Applicant Mobile 1"),
			"fieldname": "coapplicant_mobile_1",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Co-Applicant Mobile 2"),
			"fieldname": "coapplicant_mobile_2",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Enterprise Mobile 1"),
			"fieldname": "enterprise_mobile_1",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Enterprise Mobile 2"),
			"fieldname": "enterprise_mobile_2",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Restr Migr Status"),
			"fieldname": "restr_migr_status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Lead source"),
			"fieldname": "lead_source",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": ("Lead Created by"),
			"fieldname": "lead_created_by",
			"fieldtype": "Data",
			"width": 100
		},
	]
	return columns

def get_data(filters):
	data = []
	query_filters = {
		"posting_date": ['between', [filters.get("from_date"), filters.get("to_date")]],
	}

	if filters.get("partner_name"):
		query_filters.update({"co_lending_partner": filters.get("partner_name")})
	query_filters.update({"docstatus": 1})
	
	loans = frappe.get_all(
		"Loan",
		filters=query_filters,
		fields=[
			"custom_hub_1",
			"loan_officer",
			"custom_loan_officer_name",
			"co_lending_partner",
			"applicant",
			"custom_individual_applicant",
			"custom_origination_source",
			"custom_origination_source_name",
			"name",
			"loan_application_id",
			"loan_product",
			"custom_created_by",
			"rate_of_interest",
			"effective_interest_rate",
			"repayment_periods",
			"repayment_start_date",
			"disbursement_date",
			"loan_purpose",
			"loan_sub_purpose",
			"custom_sector",
			"custom_sub_sector",
			"status",
			"custom_transaction_type",
			"custom_lead_created_by"
		],
	)
	
	for loan in loans:
		
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

		coapplicant_name= frappe.db.get_value('Co Applicants',{'parent': loan.name,'idx': 1},['co_applicant'])
		applicant_name= frappe.db.get_value('Customer',coapplicant_name,['customer_name'])
		cocontact = get_contact_details(applicant_name)
		if cocontact[0] != None:
			cophone1 = cocontact[0]
		else:
			cophone1 = ''
		if cocontact[1] != None:
			cophone2 = cocontact[1]
		else:
			cophone2 = ''
		
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
			"loan_officer_id": loan.loan_officer,
			"loan_officer_name": loan.custom_loan_officer_name,
			"district": loan.region_name,
			"partner_name": loan.co_lending_partner,
			"entity_name": frappe.db.get_value('Customer',loan.applicant,'customer_name'), 
			"applicant_name": frappe.db.get_value('Customer',loan.custom_individual_applicant,'customer_name'),
			"origination_source": loan.custom_origination_source,
			"origination_source_name": loan.custom_origination_source_name,
			"account_id": loan.name,
			"kinara_application_id": loan.loan_application_id,
			"client_id": loan.custom_individual_applicant,
			"loan_product_cycle": loan_product.get("cyclic_day_of_the_month"),
			"product_code": loan.loan_product,
			"product_name": loan_product.get("product_name"),
			"created_by": loan.custom_created_by,
			"tranche_number": count_disbus,
			"total_sanction_amount": sanctioned_loan_amount,
			"tranche_disbursement_date": disbursement_date,
			"tranche_disbursed_amount": current_disbursed_amount,
			"interest_rate_pct": loan.rate_of_interest,
			"bpi_amount": bpi_amt,
			"bpi_duration_days":broken_period_interest_days,
			"iir": loan.effective_interest_rate,
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
			"account_status": loan.status,
			"applicant_mobile_1": phone1,
			"applicant_mobile_2": phone2,
			"coapplicant_mobile_1": cophone1,
			"coapplicant_mobile_2": cophone2,
			"enterprise_mobile_1": enphone1,
			"enterprise_mobile_2": enphone2,
			"transaction_type": loan.custom_transaction_type,
			"lead_created_by": loan.custom_lead_created_by
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
	