import frappe
import calendar
from datetime import datetime, timedelta

@frappe.whitelist()
def get_loan_more_response(loan):
	loans = frappe.db.get_value("Loan",loan,
		[
		"days_past_due",
		"repayment_periods",
        "is_npa",
        "manual_npa",
        "loan_product",
		"posting_date",
		"status",
		"total_amount_paid",
		"custom_legal_status",
		"custom_cpi_suggested_action",
		"custom_loan_collection_movement_status"
		],as_dict = 1
	)

	repayment_schedule = repayment_schedule_details(loan)
	nextPaymentDate = ''
	lastPaymentDate = ''
	noofEMIsRaised = ''
	noofEMIsPaid = ''
	noofEMIsOutstanding = ''
	noofEMIsOverdue = ''
	totalEMIsPaid = ''
	totalEMIsOverdue = ''
	if repayment_schedule:
		if repayment_schedule.get('nextPaymentDate'):
			nextPaymentDate = repayment_schedule.get('nextPaymentDate')
		if repayment_schedule.get('lastPaymentDate'):
			lastPaymentDate = repayment_schedule.get('lastPaymentDate')
		if repayment_schedule.get('idx'):
			noofEMIsRaised = repayment_schedule.get('idx')
			noofEMIsOverdue = noofEMIsRaised - repayment_schedule.get('emi_paid')

		if repayment_schedule.get('emi_paid'):
			noofEMIsPaid = repayment_schedule.get('emi_paid')
			noofEMIsOutstanding = loans.repayment_periods - noofEMIsPaid
		else:
			noofEMIsOutstanding = loans.repayment_periods
			
		if repayment_schedule.get('totalEMIsPaid'):
			totalEMIsPaid = repayment_schedule.get('totalEMIsPaid')

		totalEMIsOverdue = repayment_schedule.get('totalEMIsRaised') - repayment_schedule.get('totalEMIsPaid')

	if (loans.is_npa or loans.manual_npa) == 1:
		npa = 'Yes'
	else:
		npa = ''
	
	if loans.loan_product:
		product = get_product_details(loans.loan_product)
		if product:
			pir = product.get('penalty_interest_rate')
		else:
			pir = ''

	writeoff = get_writeoff_details(loan)
	writeOffDate = ''
	principalWriteOffMagnitude = ''
	if writeoff:
		if writeoff.get('posting_date'):
			writeOffDate = writeoff.get('posting_date')
		if writeoff.get('write_off_amount'):
			principalWriteOffMagnitude = writeoff.get('write_off_amount')

	securityEmiAdj = frappe.db.get_value('Loan Security Deposit',{'loan':loan},'allocated_amount')
	if securityEmiAdj == None or '':
		securityEmiAdj = ''

	if frappe.db.exists('Loan Restructure',{'loan':loan}):
		isRestructured = 'Yes'
	else:
		isRestructured = 'No'

	restructure_date = frappe.db.sql("""select restructure_date from `tabLoan Restructure` where loan=%s order by creation desc limit 1""",(loan),as_dict=True)
	totalPenal = frappe.db.sql("""select sum(paid_amount) as totalPenalPaid,sum(outstanding_amount) as totalPenalOutstanding from `tabLoan Demand` where loan=%s and demand_type = 'Penalty' and demand_subtype = 'Penalty' and docstatus = 1 """,(loan),as_dict=True)
	totalPenalPaid = totalPenal[0].get('totalPenalPaid') or ''
	totalPenalOutstanding = totalPenal[0].get('totalPenalOutstanding') or ''

	totalFeeCharges = frappe.db.sql("""select sum(paid_amount) as totalFeeChargesPaid, sum(demand_amount) as totalFeeChargesRaised, sum(outstanding_amount) as totalFeeChargesOutstanding from `tabLoan Demand` where loan=%s and demand_type = 'Charges' and demand_subtype = 'Charges' and docstatus = 1 """,(loan),as_dict=True)
	totalFeeChargesPaid = totalFeeCharges[0].get('totalFeeChargesPaid') or ''
	totalFeeChargesRaised = totalFeeCharges[0].get('totalFeeChargesRaised') or ''
	totalFeeChargesOutstanding = totalFeeCharges[0].get('totalFeeChargesOutstanding') or ''

	totalEMIsRaised = frappe.db.sql("""select sum(demand_amount) as demand_amount from `tabLoan Demand` where loan=%s and demand_type = 'EMI' and demand_subtype in ('Principal','Interest') and docstatus = 1 """,(loan),as_dict=True)[0].get('demand_amount') or ''
	totalPenalRaised = frappe.db.sql("""select sum(demand_amount) as demand_amount from `tabLoan Demand` where loan=%s and demand_type = 'Penalty' and demand_subtype = 'Penalty' and docstatus = 1 """,(loan),as_dict=True)[0].get('demand_amount') or ''
	dpdMonthEnd = get_last_day_previous_month(loan)
	row = {
		"nextPaymentDate": nextPaymentDate,
		"lastPaymentDate": lastPaymentDate,
		"dpdDays": loans.days_past_due,
		"tenure": loans.repayment_periods,
        "npaFlag": npa,
        "productName": loans.loan_product,
		"penalInterestRate": pir,
		"writeOffDate": writeOffDate,
		"principalWriteOffMagnitude": principalWriteOffMagnitude,
		"sanctionDate": loans.posting_date,
		"securityEmiAdjusted": securityEmiAdj,
		"isRestructured": isRestructured,
		"restructureDate": restructure_date or '',
		"effectiveDpd": loans.days_past_due,
		"currentStage": loans.status,
		"noofEMIsRaised": noofEMIsRaised or '',
		"noofEMIsPaid": noofEMIsPaid or '',
		"noofEMIsOutstanding": noofEMIsOutstanding,
		"noofEMIsOverdue": noofEMIsOverdue,
		"totalEMIsPaid": totalEMIsPaid,
		"totalEMIsOverdue": totalEMIsOverdue,
		"totalPenalPaid": totalPenalPaid,
		"totalPenalOutstanding": totalPenalOutstanding,
		"totalFeeChargesPaid": totalFeeChargesPaid,
		"totalFeeChargesRaised": totalFeeChargesRaised,
		"totalFeeChargesOutstanding": totalFeeChargesOutstanding,
		"paidAmountMagnitude": loans.total_amount_paid,
		"totalEMIsRaised": totalEMIsRaised,
		"totalPenalRaised": totalPenalRaised,
		"writeOffprincipalDue": '',
		"writeOffInterestOverdue": '',
		"writeOffPenalInterestOverdue": '',
		"writeOffBookedNotDuePenalInterest":'',
		"writeOffFeeDue": '',
		"legalStatus": loans.custom_legal_status or '',
		"cpiSuggestedAction": loans.custom_cpi_suggested_action or '',
		"loanCollectionMovementStatus": loans.custom_loan_collection_movement_status or '',
		"dpdMonthEnd": dpdMonthEnd or ''
		}
	return row

def repayment_schedule_details(loan):
	repayment_schedule_data = {}
	loan_repayment = frappe.db.sql("""select name from `tabLoan Repayment Schedule` where loan=%s and status = "Active" order by creation desc limit 1""",(loan),as_dict=True)
	if loan_repayment:
		loan_repayment_doc = frappe.get_doc("Loan Repayment Schedule",loan_repayment[0].get("name"))
		count = 0
		totalEMIsPaid = 0
		totalEMIsRaised = 0
		for i in loan_repayment_doc.repayment_schedule:
			if i.demand_generated == 0:
				repayment_schedule_data.update({'idx':i.idx - 1}) # idx is total number of EMI's Raised
				nextPaymentDate = i.payment_date
				repayment_schedule_data.update({'nextPaymentDate':nextPaymentDate})
				if i.idx > 0:
					lastPaymentDate = frappe.db.get_value('Repayment Schedule',{'parent':loan_repayment[0].get("name"),'idx':i.idx - 1},'payment_date')
					repayment_schedule_data.update({'lastPaymentDate':lastPaymentDate})
				break
			
			#For Numbers of EMI's Paid 
			if i.demand_generated == 1:
				totalEMIsRaised += i.total_payment
				if frappe.db.get_value('Loan Demand',{'repayment_schedule_detail':i.name,'docstatus': 1,'demand_type': 'EMI','demand_subtype': 'Principal'},'outstanding_amount') == 0:
					totalEMIsPaid += i.total_payment
					count += 1
		repayment_schedule_data.update({'totalEMIsRaised':totalEMIsRaised})
		repayment_schedule_data.update({'totalEMIsPaid':totalEMIsPaid})
		repayment_schedule_data.update({'emi_paid':count})

	return repayment_schedule_data

def get_product_details(loan):
	loan_product = frappe.db.get_value("Loan Product",{'name':loan},[
		"penalty_interest_rate"
		],as_dict = 1)
	if loan_product:
		return loan_product

def get_writeoff_details(loan):
	loan_product = frappe.db.get_value("Loan Write Off",{'loan':loan},[
		"posting_date",
		"write_off_amount"
		],as_dict = 1)
	if loan_product:
		return loan_product

def get_last_day_previous_month(loan):

	# Get the current date
	current_date = datetime.now()

	# Calculate the first day of the current month
	first_day_of_current_month = current_date.replace(day=1)

	# Calculate the last day of the previous month
	last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)

	# Print the result in the desired format
	formatted_result = last_day_of_previous_month.strftime('%Y-%m-%d')
	dpdMonthEnd = frappe.db.get_value('Days Past Due Log',{'loan':loan,'posting_date':formatted_result},'days_past_due')
	return dpdMonthEnd
