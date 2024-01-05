import frappe
from datetime import datetime

@frappe.whitelist()
def get_loan_list(hub=None,loan_account_number=None,customer_urn=None,customer_name=None):
	filters = {}
	loan = ''
	if hub != None:
		filters["hub"] = hub
	if loan_account_number != None:
		filters["loan_account_number"] = loan_account_number
	if customer_name:
		customer_name = frappe.db.get_value('Customer',{'customer_name':customer_name},'customer_urn')
	if not customer_urn  and customer_name:
		filters["applicant"] = customer_name
	if customer_urn  and not customer_name:
		filters["applicant"] = customer_urn
	if (customer_urn and customer_name) and (customer_urn  == customer_name):
		filters["applicant"] = customer_urn
	if filters != {}:
		loan = frappe.db.get_list('Loan',filters = filters, pluck='name')
	if (customer_urn and customer_name) and (customer_urn  != customer_name):
		a = []
		loan_urn = frappe.db.get_list('Loan',filters = {'applicant':customer_urn}, pluck='name')
		a.extend(loan_urn)
		loan_name = frappe.db.get_list('Loan',filters = {'applicant':customer_name}, pluck='name')
		a.extend(loan_name)
		if loan:
			loan.extend(a)
		else:
			loan = a
	return loan

@frappe.whitelist()
def get_outstanding_principal(**kwargs):
	where_clause = ""
	join_clause = ""
	if kwargs["group_by"] in ["branch", "hub_code", "hub_name", "hub_id", "zone_name", "zone_code", "division", "division_code", "region_name", "region_code"]:
		if kwargs["group_by"] == "branch":
			group_by = f"loan.{kwargs['group_by']}"
		else:
			join_clause = "JOIN `tabBranch` as branch ON loan.branch = branch.branch"
			group_by = f"branch.{kwargs['group_by']}"
		if "group_by_value" in kwargs and kwargs["group_by_value"]:
			where_clause = f"""WHERE {group_by} = "{kwargs["group_by_value"]}" """
	else:
		return {"error": "Invalid group_by Parameter. Valid group_by Parameters are: branch/hub_code/hub_name/hub_id/zone_name/zone_code/division/division_code/region_name/region_code"}
	outstanding_principal = frappe.db.sql(f"""
											SELECT
												{group_by}, SUM(loan.total_payment - loan.total_interest_payable - loan.total_principal_paid) as outstanding_principal
											FROM `tabLoan` as loan
											{join_clause}
											{where_clause}
											GROUP BY {group_by}
											""", as_dict = True)
	return outstanding_principal


@frappe.whitelist()
def get_loan_ach_not_active(**kwargs):
    loan_list = frappe.db.sql("""SELECT DISTINCT loan.name as 'loan', business.customer_name as 'business_name', loan.loan_amount as 'loan_amount', applicant.customer_name as 'applicant_name'
                                    FROM `tabLoan ACH` as loan_ach
                                    JOIN `tabLoan` as loan
                                        ON loan.name = loan_ach.loan
									LEFT JOIN `tabCustomer` as business
							  			ON business.customer_urn = loan.applicant
							  		LEFT JOIN `tabCustomer` as applicant
							  			ON applicant.customer_urn = loan.custom_individual_applicant
                                    WHERE loan_ach.docstatus = 0""", as_dict = True)
    return loan_list

@frappe.whitelist()
def get_loan_pdc_not_active(**kwargs):
    loan_list = frappe.db.sql("""SELECT DISTINCT loan.name as 'loan', business.customer_name as 'business_name', loan.loan_amount as 'loan_amount', applicant.customer_name as 'applicant_name'
                                    FROM `tabLoan PDC` as loan_pdc
                                    JOIN `tabLoan` as loan
                                        ON loan_pdc.loan = loan.name
							  		LEFT JOIN `tabCustomer` as business
							  			ON business.customer_urn = loan.applicant
							  		LEFT JOIN `tabCustomer` as applicant
							  			ON applicant.customer_urn = loan.custom_individual_applicant
                                    WHERE loan_pdc.status != "Active" """, as_dict = True)
    return loan_list

@frappe.whitelist()
def get_loan_partial_pdc(**kwargs):
    loan_list = frappe.db.sql("""SELECT DISTINCT loan.name as 'loan', business.customer_name as 'business_name', loan.loan_amount as 'loan_amount', applicant.customer_name as 'applicant_name'
                                    FROM `tabLoan` AS loan
                                    JOIN `tabLoan Repayment Schedule` AS loan_repayment_schedule
                                        ON loan_repayment_schedule.loan = loan.name
                                    JOIN `tabRepayment Schedule` AS repayment_schedule
                                        ON repayment_schedule.parent = loan_repayment_schedule.name
                                    JOIN `tabLoan PDC` AS loan_pdc
                                        ON loan_pdc.loan = loan.name
                                        AND loan_pdc.loan_repayment_schedule = loan_repayment_schedule.name
							  		LEFT JOIN `tabCustomer` as business
							  			ON business.customer_urn = loan.applicant
							  		LEFT JOIN `tabCustomer` as applicant
							  			ON applicant.customer_urn = loan.custom_individual_applicant
                                    WHERE NOT EXISTS (SELECT 1
                                        FROM `tabLoan PDC` AS lp
                                        WHERE lp.name = loan_pdc.name
                                        	AND lp.emi = repayment_schedule.name)
                                        """, as_dict = True)
    return loan_list

@frappe.whitelist()
def get_mandate_details_ach_not_active(**kwargs):
	loan_list = get_loan_ach_not_active()
	loans = ', '.join([f"'{loan}'" for loan in loan_list])
	loan_details = frappe.db.sql(f"""SELECT *
							  		FROM `tabLoan`
							  		WHERE name IN ({loans})""", as_dict=True)
	return "underdevelopment"