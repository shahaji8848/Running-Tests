# Copyright (c) 2024, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime
from datetime import timedelta
from frappe.utils import flt
from frappe.utils import (
	add_days,
	add_months,
	add_years,
	cint,
	cstr,
	date_diff,
	flt,
	formatdate,
	get_last_day,
	get_timestamp,
	getdate,
	nowdate,
)
from erpnext.accounts.utils import get_fiscal_year

def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data

def get_columns():
	columns = [
		{
			"label": ("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 100
		},
		{
			"label": ("Total Principal Outstanding"),
			"fieldname": "total_prin_os",
			"fieldtype": "Data",
			"width": 205
		},
		{
			"label": ("90+ Days Principal Outstanding"),
			"fieldname": "90_days_prin_os",
			"fieldtype": "Data",
			"width": 235
		},
		{
			"label": ("1 to 90 Days PrinOD SchedBal"),
			"fieldname": "1to90_days_prinod_schedbal",
			"fieldtype": "Data",
			"width": 235
		},
		{
			"label": ("Weighted Avg Interest "),
			"fieldname": "weighted_avg_interest",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": ("POS For Interest"),
			"fieldname": "pos_for_interest",
			"fieldtype": "Data",
			"width": 120
		},
		{
			"label": ("Interest Income"),
			"fieldname": "interest_income",
			"fieldtype": "Data",
			"width": 120
		}
	]
	return columns

def get_data(filters):
	data = []
	start = datetime.strptime(filters.get("from_date"), "%Y-%m-%d").date()
	end = datetime.strptime(filters.get("to_date"), "%Y-%m-%d").date()
	
	for delta in range((end - start).days + 1):
		result_date = start + timedelta(days=delta)
		loans = frappe.get_all("Loan",filters={'posting_date': result_date.strftime("%Y-%m-%d"),'status': ['in', ['Disbursed', 'Partially Disbursed', 'Active']],},fields=
			[
			"posting_date",
			"status",
			"total_payment",
			"total_principal_paid",
			"total_interest_payable",
			"written_off_amount",
			"days_past_due",
			"loan_product",
			"name"
			],)

		total_pos = 0
		ninty_plus_pos = 0
		ninty_btw_pos = 0
		total_pdt_rate = 0
		count = 0
		weighted_avg_interest=0
		interest_income = 0
		for loan in loans:
			if loan:
				pos = flt(loan.get('total_payment'))- flt(loan.get('total_principal_paid'))- flt(loan.get('total_interest_payable'))- flt(loan.get('written_off_amount'))
				total_pos += pos
				accrual = frappe.db.sql("""select interest_amount from `tabLoan Interest Accrual` where loan=%s and docstatus = 1 order by creation desc limit 1""",(loan.get('name')),as_dict=True)
				if accrual:
					interest_income += accrual[0].get('interest_amount')

			if loan.get('days_past_due') > 90:
				pos_ninty_plus = flt(loan.get('total_payment'))- flt(loan.get('total_principal_paid'))- flt(loan.get('total_interest_payable'))- flt(loan.get('written_off_amount'))
				ninty_plus_pos += pos_ninty_plus

			if 1 <= loan.get('days_past_due') <= 90:
				a = flt(loan.get('total_payment'))- flt(loan.get('total_principal_paid'))- flt(loan.get('total_interest_payable'))- flt(loan.get('written_off_amount'))
				ninty_btw_pos += a

			if loan.get('loan_product'):
				loan_pdt = frappe.db.get_value('Loan Product',loan.get('loan_product'),'rate_of_interest')
				total_pdt_rate += loan_pdt
				count += 1
			weighted_avg_interest = flt(total_pdt_rate)/flt(count)
		
		current_fiscal_year = get_fiscal_year(nowdate(), as_dict=True)
		diff = date_diff(result_date.strftime("%Y-%m-%d"),current_fiscal_year.year_start_date)
		pos_for_interest = (total_pos*weighted_avg_interest)/365*diff
		
		row = {
			"date": result_date.strftime("%Y-%m-%d"),
			"total_prin_os": total_pos,
			"90_days_prin_os": ninty_plus_pos,
			"1to90_days_prinod_schedbal": ninty_btw_pos,
			"weighted_avg_interest": weighted_avg_interest,
			"pos_for_interest": pos_for_interest,
			"interest_income": interest_income
		}
		data.append(row)
	return data
