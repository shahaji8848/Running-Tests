# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe


def execute(filters=None):
	columns = [
				"partner_name",
				"Zone",
				"State",
				"Division",
				"Region",
				"Parent Branch",
				"Hub",
				"ClientID",
				"AccountID",
				"ProductName",
				"ClientName",
				"Proprietor Name",
				"InstallmentDueDate",
				"LoanAmount",
				"Cheque ID",
				"Current Due",
				"installment_number",
				"Term",
				"Repayment Mode",
				"Bank Name",
				"Branch Name",
				"Realization Status",
				"Realization Reason",
				"Realization Date",
				"Mobile No."
			]
	data = get_loan_demand_data(filters)
	return columns, data

def get_loan_demand_data(filters):
	
	conditions = [f"demand.docstatus = 1"]
	subquery_conditions = [
					f"ld.demand_type = 'EMI'", 
					f"ld.docstatus = 1"
				]
	
	if filters.report_type:
		report_type = filters.report_type
	else:
		report_type = 'scheduled'
		
	if filters.to_date and filters.from_date:
		if filters.from_date > filters.to_date:
			frappe.throw("From Date cannot be greater than To Date")
		from_date = filters.from_date
		to_date = filters.to_date
	else:
		date = frappe.db.sql(f"""SELECT demand.demand_date
					   			FROM `tabLoan Demand` as demand
					   			WHERE demand.demand_type = 'EMI'
					   			ORDER BY demand.demand_date DESC
								LIMIT 1
								""")
		from_date = date[0]
		to_date = date[0]

	conditions.append(f"demand.demand_date <= '{to_date}' ")
	conditions.append(f"demand.demand_date >= '{from_date}' ")
	order_by = ""
	if report_type == "scheduled":	
		conditions.append(f"demand.demand_type = 'EMI'")
		subquery_conditions.append(f"ld.demand_date = '{to_date}'")
	elif report_type == "overdue":
		subquery_conditions.append(f"ld.demand_date <= '{to_date}'")
		order_by = "ORDER BY installment_details.payment_date DESC"
	
	where_clause = "WHERE " + " AND ".join(conditions)
	subquery_where_clause = "WHERE " + " AND ".join(subquery_conditions)

	demands_details  = frappe.db.sql(f"""
									SELECT COALESCE(NULLIF(co_lending_partner.partner_name,''), NULLIF(loan_channel_partner.name1,''), loan.company) as "partner_name",
										branch.zone_name as "Zone",
										branch.state as "State",
										branch.division as "Division",
										branch.region_name as "Region",
										branch.region_name as "Parent Branch",
										loan.hub as "Hub",
										loan.applicant as "ClientID",
										loan.name as "AccountID", 
										loan_product.product_name as "ProductName",
										entity.customer_name as "ClientName", 
										applicant.customer_name as "Proprietor Name", 
										installment_details.payment_date as "InstallmentDueDate",
										loan.loan_amount as "LoanAmount", 
										SUM(demand.demand_amount - demand.paid_amount) as "Current Due", 
										installment_details.idx as "installment_number", 
										loan_repayment_schedule.repayment_periods as "Term",
										loan_repayment.repayment_mode as "Repayment Mode", 
										demand_details.realization_status as "Realization Status", 
										demand_details.realization_reason as "Realization Reason", 
										demand_details.realization_date as "Realization Date",
										entity.mobile_no as "Mobile No",
										demand_details.name as "Demand Name"
									FROM `tabLoan Demand` as demand
										LEFT JOIN `tabLoan` as loan ON demand.loan = loan.name
										LEFT JOIN `tabLoan Repayment` as loan_repayment ON loan_repayment.against_loan = loan.name
										LEFT JOIN `tabCustomer` as entity ON entity.name = loan.applicant
										LEFT JOIN `tabCustomer` as applicant ON applicant.name = loan.custom_individual_applicant
										LEFT JOIN `tabLoan Product` as loan_product ON loan_product.name = loan.loan_product
										LEFT JOIN `tabLoan Demand` as demand_details ON demand_details.name = (SELECT ld.name
																												FROM `tabLoan Demand` as ld
																												{subquery_where_clause} AND ld.loan = loan.name
																												ORDER BY ld.demand_date DESC, ld.modified DESC
																												LIMIT 1)
										LEFT JOIN `tabRepayment Schedule` as installment_details ON installment_details.name = demand_details.repayment_schedule_detail
										LEFT JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule ON loan_repayment_schedule.name = installment_details.parent
										LEFT JOIN `tabLoan Partner` as co_lending_partner ON co_lending_partner.name = loan.co_lending_partner
										LEFT JOIN `tabLoan Channel Partner` as loan_channel_partner ON loan_channel_partner.name = loan.custom_channel_partner
										LEFT JOIN `tabBranch` as branch ON loan.hub = branch.name
										{where_clause}
										GROUP BY demand.loan, demand.demand_date
										{order_by}""", as_dict=1)

	response = []
	for demand_detail in demands_details:
		response_doc = {
			"partner_name" : demand_detail["partner_name"],
			"Zone" : demand_detail["Zone"],
			"State" : demand_detail["State"],
			"Division": demand_detail["Division"],
			"Region": demand_detail["Region"],
			"Parent Branch": demand_detail["Parent Branch"],
			"Hub": demand_detail["Hub"],
			"ClientID": demand_detail["ClientID"],
			"AccountID": demand_detail["AccountID"],
			"ProductName": demand_detail["ProductName"],
			"ClientName": demand_detail["ClientName"],
			"Proprietor Name": demand_detail["Proprietor Name"],
			"InstallmentDueDate": demand_detail["InstallmentDueDate"],
			"LoanAmount": demand_detail["LoanAmount"],
			"Cheque ID": None,
			"Current Due": demand_detail["Current Due"],
			"installment_number": demand_detail["installment_number"],
			"Term": demand_detail["Term"],
			"Repayment Mode": demand_detail["Repayment Mode"],
			"Bank Name": None,
			"Branch Name": None,
			"Realization Status": demand_detail["Realization Status"],
			"Realization Reason": demand_detail["Realization Reason"],
			"Realization Date": demand_detail["Realization Date"],
			"Mobile No.": demand_detail["Mobile No"],
		}
		if demand_detail["Repayment Mode"] == "ACH":
			ach = frappe.db.sql(f"""
								SELECT ach.bank_name as "Bank Name", ach.branch_name as "Branch Name"
								FROM `tabLoan ACH` as ach
								WHERE ach.loan = '{demand_detail["AccountID"]}'
								AND ach.docstatus = 1
								ORDER BY ach.modified DESC
								LIMIT 1""", as_dict=1)
			if len(ach) > 0:
				response_doc["Bank Name"] = ach[0]["Bank Name"]
				response_doc["Branch Name"] = ach[0]["Branch Name"]
		if demand_detail["Repayment Mode"] == "PDC":
			pdc = frappe.db.sql(f"""
								SELECT pdc.bank_name as "Bank Name", pdc.branch_name as "Branch Name", pdc.cheque_number as "Cheque ID"
								FROM `tabLoan PDC` as pdc
								WHERE pdc.emi = '{demand_detail["Demand Name"]}'
								AND pdc.status = 'Active'
								ORDER BY pdc.modified DESC
								LIMIT 1""", as_dict=1)
			if len(pdc) > 0:
				response_doc["Bank Name"] = pdc[0]["Bank Name"]
				response_doc["Branch Name"] = pdc[0]["Branch Name"]
				response_doc["Cheque ID"] = pdc[0]["Cheque ID"]
		if demand_detail["Demand Name"] == None:
			subquery_conditions.pop(0)
			subquery_conditions.append(f"""ld.loan = '{demand_detail["AccountID"]}'""")
			subquery_where_clause = "WHERE " + " AND ".join(subquery_conditions)
			frappe.response["message"] = subquery_where_clause
			latest_realization = frappe.db.sql(f"""
												SELECT ld.realization_status as "Realization Status", 
													ld.realization_reason as "Realization Reason", 
													ld.realization_date as "Realization Date"
												FROM `tabLoan Demand` as ld
												{subquery_where_clause}
												ORDER BY ld.demand_date DESC, ld.modified DESC
												LIMIT 1""", as_dict=1)
			if len(latest_realization):
				response_doc["Realization Status"] = latest_realization[0]["Realization Status"]
				response_doc["Realization Reason"] = latest_realization[0]["Realization Reason"]
				response_doc["Realization Date"] = latest_realization[0]["Realization Date"]
		response.append(response_doc)
	two_d_list = [[entry[key] for key in entry]for entry in response]
	return two_d_list
