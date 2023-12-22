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
	loan_ach_list = frappe.db.sql(f"""SELECT ln.name
									FROM `tabLoan` as ln
									WHERE ln.name NOT IN (
    									SELECT loan.name
    									FROM `tabLoan` as loan
    									JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule 
							   			ON loan_repayment_schedule.loan = loan.name
    									JOIN `tabRepayment Schedule` as repayment_schedule 
							   			ON loan_repayment_schedule.name = repayment_schedule.parent
    									JOIN `tabLoan PDC` as loan_pdc 
							   			ON loan_pdc.emi = repayment_schedule.name
    								WHERE loan_repayment_schedule.status = "Active"
									)""", as_dict = True)
	response = []
	for loan in loan_ach_list:
		loan_account_valid = False
		response_doc = {}
		response_doc["Loan Account No"] = loan['name']
		loan_ach_doc_list = frappe.db.sql(f"""SELECT DISTINCT loan_ach.name as loan_ach_name, loan_repayment_schedule.name as loan_repayment_schedule_name
						   			FROM `tabLoan ACH` as loan_ach
						   			JOIN `tabLoan` as loan
						   			ON loan_ach.loan = "{loan['name']}"
									JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule
									ON loan_repayment_schedule.loan = "{loan['name']}"
									WHERE loan_repayment_schedule.status = "Active"
									AND loan.name = "{loan['name']}"
									""", as_dict = True)
		if len(loan_ach_doc_list) == 0:
			response_doc["Loan PDC"] = None
			response_doc["Loan ACH"] = None
		else:
			response_doc["Loan ACH"] = []
			for loan_ach_doc in loan_ach_doc_list:
				loan_ach_dict = {}
				loan_ach_dict["ACH Registration Number"] = loan_ach_doc['loan_ach_name']
				loan_ach_dict['Loan Repayment Schedule'] = loan_ach_doc['loan_repayment_schedule_name']
				docstatus, ach_start_date,  ach_end_date = frappe.db.get_value('Loan ACH', loan_ach_doc['loan_ach_name'], ['docstatus', 'ach_start_date', 'ach_end_date'])
				loan_ach_dict["Loan ACH Docstatus"] = docstatus
				if docstatus == 1:
					loan_repayment_schedule = frappe.get_doc('Loan Repayment Schedule', loan_ach_doc['loan_repayment_schedule_name'])
					loan_repayment_schedule_start_date = loan_repayment_schedule.repayment_schedule[0].payment_date
					loan_repayment_schedule_end_date = loan_repayment_schedule.repayment_schedule[len(loan_repayment_schedule.repayment_schedule)-1].payment_date
					if ach_start_date <= loan_repayment_schedule_start_date and ach_end_date >= loan_repayment_schedule_end_date:
						loan_account_valid = True
						break
					else:
						loan_ach_dict['First EMI Date'] = loan_repayment_schedule_start_date
						loan_ach_dict['Last EMI Date'] = loan_repayment_schedule_end_date
						loan_ach_dict['ACH Start Date'] = ach_start_date
						loan_ach_dict['ACH End Date'] = ach_end_date
				response_doc["Loan ACH"].append(loan_ach_dict)
		if not loan_account_valid:
			response.append(response_doc)
	return response



@frappe.whitelist()
def get_loan_pdc_not_active(**kwargs):
	loan_pdc_list = frappe.db.sql(f"""SELECT DISTINCT loan.name
    								FROM `tabLoan` as loan
    								JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule 
							   		ON loan_repayment_schedule.loan = loan.name
    								JOIN `tabRepayment Schedule` as repayment_schedule 
							   		ON loan_repayment_schedule.name = repayment_schedule.parent
    								JOIN `tabLoan PDC` as loan_pdc 
							   		ON loan_pdc.emi = repayment_schedule.name
    								WHERE loan_repayment_schedule.status = "Active"
									""", as_dict = True)
	response = []
	for loan in loan_pdc_list:
		loan_account_valid = True
		response_doc = {}
		response_doc["Loan Account No"] = loan['name']
		active_repayment_schedule_list = frappe.db.sql(f"""SELECT DISTINCT loan_repayment_schedule.name as loan_repayment_schedule_name
						   			FROM `tabLoan Repayment Schedule` as loan_repayment_schedule
						   			JOIN `tabLoan` as loan						
									ON loan_repayment_schedule.loan = "{loan['name']}"
									WHERE loan_repayment_schedule.status = "Active"
									AND loan.name = "{loan['name']}"
									""", as_dict = True)
		if len(active_repayment_schedule_list) == 0:
			response_doc["Loan PDC"] = None
		else:
			response_doc["Loan Repayment Schedule List"] = []
			for active_repayment_schedule in active_repayment_schedule_list:
				active_repayment_schedule_dict = {}
				active_repayment_schedule_dict['Loan Repayment Schedule'] = active_repayment_schedule['loan_repayment_schedule_name']
				active_repayment_schedule_dict['Loan PDC List'] = []
				loan_pdc_list = frappe.db.sql(f"""SELECT DISTINCT loan_pdc.name AS loan_pdc_name
												FROM `tabLoan PDC` AS loan_pdc
												JOIN `tabLoan Repayment Schedule` AS loan_repayment_schedule 
								  				ON loan_pdc.loan_repayment_schedule = "{active_repayment_schedule['loan_repayment_schedule_name']}"
												JOIN `tabRepayment Schedule` AS repayment_schedule 
								  				ON loan_pdc.emi = repayment_schedule.name AND loan_repayment_schedule.name = "{active_repayment_schedule['loan_repayment_schedule_name']}"
												WHERE loan_pdc.loan = "{loan['name']}" """, as_dict = True)
				for loan_pdc in loan_pdc_list:
					loan_pdc_dict = {}
					loan_pdc_status = frappe.db.get_value('Loan PDC', loan_pdc['loan_pdc_name'], ['status'])
					if loan_pdc_status != "Active":
						loan_account_valid = False
						loan_pdc_dict['PDC'] = loan_pdc['loan_pdc_name']
						loan_pdc_dict['Status'] = loan_pdc_status
						active_repayment_schedule_dict['Loan PDC List'].append(loan_pdc_dict)
				response_doc["Loan Repayment Schedule List"].append(active_repayment_schedule_dict)
		if not loan_account_valid:
			response.append(response_doc)
	return response

@frappe.whitelist()
def get_loan_partial_pdc(**kwargs):
	loan_pdc_list = frappe.db.sql(f"""SELECT DISTINCT loan.name
    								FROM `tabLoan` as loan
    								JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule 
							   		ON loan_repayment_schedule.loan = loan.name
    								JOIN `tabRepayment Schedule` as repayment_schedule 
							   		ON loan_repayment_schedule.name = repayment_schedule.parent
    								JOIN `tabLoan PDC` as loan_pdc 
							   		ON loan_pdc.emi = repayment_schedule.name
    								WHERE loan_repayment_schedule.status = "Active"
									""", as_dict = True)
	response = []
	for loan in loan_pdc_list:
		loan_account_valid = True
		response_doc = {}
		response_doc["Loan Account No"] = loan['name']
		active_repayment_schedule_list = frappe.db.sql(f"""SELECT DISTINCT loan_repayment_schedule.name as loan_repayment_schedule_name
						   			FROM `tabLoan Repayment Schedule` as loan_repayment_schedule
						   			JOIN `tabLoan` as loan						
									ON loan_repayment_schedule.loan = "{loan['name']}"
									WHERE loan_repayment_schedule.status = "Active"
									AND loan.name = "{loan['name']}"
									""", as_dict = True)
		if len(active_repayment_schedule_list) == 0:
			response_doc["Loan PDC"] = None
		else:
			response_doc["Loan Repayment Schedule List"] = []
			for active_repayment_schedule in active_repayment_schedule_list:
				active_repayment_schedule_dict = {}
				active_repayment_schedule_dict['Loan Repayment Schedule'] = active_repayment_schedule['loan_repayment_schedule_name']
				active_repayment_schedule_dict['Missing EMI PDC'] = []
				loan_pdc_list = frappe.db.sql(f"""SELECT DISTINCT loan_pdc.name AS loan_pdc_name
												FROM `tabLoan PDC` AS loan_pdc
												JOIN `tabLoan Repayment Schedule` AS loan_repayment_schedule 
								  				ON loan_pdc.loan_repayment_schedule = "{active_repayment_schedule['loan_repayment_schedule_name']}"
												JOIN `tabRepayment Schedule` AS repayment_schedule 
								  				ON loan_pdc.emi = repayment_schedule.name AND loan_repayment_schedule.name = "{active_repayment_schedule['loan_repayment_schedule_name']}"
												WHERE loan_pdc.loan = "{loan['name']}" """)
				flattened_loan_pdc_list = [item for sublist in loan_pdc_list for item in sublist]
				loan_repayment_schedule_doc = frappe.get_doc("Loan Repayment Schedule", active_repayment_schedule['loan_repayment_schedule_name'])
				if len(loan_repayment_schedule_doc.repayment_schedule) != len(loan_pdc_list):
					loan_account_valid = False
					loan_pdc_emi_list = frappe.db.sql("""SELECT loan_pdc.emi
    													FROM `tabLoan PDC` AS loan_pdc
    													WHERE loan_pdc.name IN (%s)""", (flattened_loan_pdc_list,))
					flattened_loan_pdc_emi_list = [item for sublist in loan_pdc_emi_list for item in sublist]
					active_repayment_schedule_dict['Missing EMI PDC'].extend(
    					[row.idx for row in loan_repayment_schedule_doc.repayment_schedule 
		  					if not any(row.name == name for name in flattened_loan_pdc_emi_list)])
				response_doc["Loan Repayment Schedule List"].append(active_repayment_schedule_dict)
		if not loan_account_valid:
			response.append(response_doc)
	return response