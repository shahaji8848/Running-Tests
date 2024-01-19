import frappe

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