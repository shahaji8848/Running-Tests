import frappe

@frappe.whitelist()
def get_prod_attr(product):
    if product != None:
        values = {'product': product}
        data = {}
        loan_partner = frappe.db.sql("""
            SELECT
                IfNull(GROUP_CONCAT(DISTINCT loan_partner), '') AS loan_partners
                from `tabLoan Product Loan Partner`
            WHERE parent = %(product)s
        """, values=values, as_dict=1)

        if loan_partner:
            data.update(loan_partner[0])
        charge_type = frappe.db.sql("""
            SELECT
                IfNull(GROUP_CONCAT(DISTINCT charge_type), '') AS charge_type
                from  `tabLoan Charges`
            WHERE parent = %(product)s
        """, values=values, as_dict=1)
        if charge_type:
            data.update(charge_type[0])

        data1 = frappe.db.sql("""
            SELECT
                IfNull(lp.name,'') AS name,
                IfNull(lp.creation,'') AS creation,
                IfNull(lp.docstatus,'') AS docstatus,
                IfNull(lp.idx,'') AS idx,
                IfNull(lp.loan_name,'') AS loan_name,
                IfNull(lp.maximum_loan_amount,'') AS maximum_loan_amount,
                IfNull(lp.rate_of_interest,'') AS rate_of_interest,
                IfNull(lp.penalty_interest_rate,'') AS penalty_interest_rate,
                IfNull(lp.grace_period_in_days,'') AS grace_period_in_days,
                IfNull(lp.write_off_amount,'') AS write_off_amount,
                IfNull(lp.company,'') AS company,
                IfNull(lp.is_term_loan,'') AS is_term_loan,
                IfNull(lp.disabled,'') AS disabled,
                IfNull(lp.repayment_schedule_type,'') AS repayment_schedule_type,
                IfNull(lp.repayment_date_on,'') AS repayment_date_on,
                IfNull(lp.days_past_due_threshold_for_npa,'') AS days_past_due_threshold_for_npa,
                IfNull(lp.description,'') AS description,
                IfNull(lp.mode_of_payment,'') AS mode_of_payment,
                IfNull(lp.disbursement_account,'') AS disbursement_account,
                IfNull(lp.payment_account,'') AS payment_account,
                IfNull(lp.suspense_interest_receivable,'') AS suspense_interest_receivable,
                IfNull(lp.suspense_interest_income,'') AS suspense_interest_income,
                IfNull(lp.suspense_collection_account,'') AS suspense_collection_account,
                IfNull(lp.loan_account,'') AS loan_account,
                IfNull(lp.interest_income_account,'') AS interest_income_account,
                IfNull(lp.interest_receivable_account,'') AS interest_receivable_account,
                IfNull(lp.penalty_receivable_account,'') AS penalty_receivable_account,
                IfNull(lp.charges_receivable_account,'') AS charges_receivable_account,
                IfNull(lp.penalty_income_account,'') AS penalty_income_account,
                IfNull(lp.security_deposit_account,'') AS security_deposit_account,
                IfNull(lp.principal_waiver_account,'') AS principal_waiver_account,
                IfNull(lp.interest_waiver_account,'') AS interest_waiver_account,
                IfNull(lp.penalty_waiver_account,'') AS penalty_waiver_account,
                IfNull(lp.charges_waiver_account,'') AS charges_waiver_account,
                IfNull(lp.charges_waiver_item,'') AS charges_waiver_item,
                IfNull(lp.amended_from,'') AS amended_from,
                IfNull(lp.loan_category,'') AS loan_category,
                IfNull(lp.cyclic_day_of_the_month,'') AS cyclic_day_of_the_month,
                IfNull(lp.product_code,'') AS product_code,
                IfNull(lp.product_name,'') AS product_name,
                IfNull(lp.penalty_interest_method,'') AS penalty_interest_method,
                IfNull(lp.penalty_interest_value_ptpd,'') AS penalty_interest_value_ptpd,
                IfNull(lp.broken_period_interest_charged,'') AS broken_period_interest_charged,
                IfNull(lp.auto_close_with_security_deposit,'') AS auto_close_with_security_deposit,
                IfNull(lp.min_auto_closure_tolerance_amount,'') AS min_auto_closure_tolerance_amount,
                IfNull(lp.max_auto_closure_tolerance_amount,'') AS max_auto_closure_tolerance_amount,
                IfNull(lp.min_days_bw_disbursement_first_repayment,'') AS min_days_bw_disbursement_first_repayment,
                IfNull(lp.interest_accrued_account,'') AS interest_accrued_account,
                IfNull(lp.broken_period_interest_recovery_account,'') AS broken_period_interest_recovery_account,
                IfNull(lp.same_as_regular_interest_accounts,'') AS same_as_regular_interest_accounts,
                IfNull(lp.additional_interest_income,'') AS additional_interest_income,
                IfNull(lp.additional_interest_accrued,'') AS additional_interest_accrued,
                IfNull(lp.additional_interest_receivable,'') AS additional_interest_receivable,
                IfNull(lp.additional_interest_suspense,'') AS additional_interest_suspense,
                IfNull(lp.additional_interest_waiver,'') AS additional_interest_waiver,
                IfNull(lp.penalty_accrued_account,'') AS penalty_accrued_account,
                IfNull(lp.penalty_suspense_account,'') AS penalty_suspense_account,
                IfNull(lp.write_off_account,'') AS write_off_account,
                IfNull(lp.write_off_recovery_account,'') AS write_off_recovery_account,
                IfNull(lp.custom_is_moratorium_allowed,'') AS custom_is_moratorium_allowed,
                IfNull(lp.custom_is_moratorium_types_allowed,'') AS custom_is_moratorium_types_allowed,
                IfNull(lp.custom_moratorium_on_1st_disbursement,'') AS custom_moratorium_on_1st_disbursement,
                IfNull(lp.custom_moratorum_duration,'') AS custom_moratorum_duration,
                IfNull(lp.custom_moratorium_types_allowed,'') AS custom_moratorium_types_allowed,
                IfNull(lp.custom_repayment_method,'') AS custom_repayment_method,
                IfNull(lp.custom_repayment_demand_frequency,'') AS custom_repayment_demand_frequency,
                IfNull(lp.custom_day_count_convention,'') AS custom_day_count_convention,
                IfNull(lp.custom_advance_payment_allowed,'') AS custom_advance_payment_allowed,
                IfNull(lp.custom_partial_payment_allowed,'') AS custom_partial_payment_allowed,
                IfNull(lp.custom_part_prepayment_allowed,'') AS custom_part_prepayment_allowed,
                IfNull(lp.custom_foreclosure_allowed,'') AS custom_foreclosure_allowed,
                IfNull(lp.custom_minimum_tenure,'') AS custom_minimum_tenure,
                IfNull(lp.custom_maximum_tenure,'') AS custom_maximum_tenure,
                IfNull(lp.custom_default_tenure,'') AS custom_default_tenure,
                IfNull(lp.custom_roi_type,'') AS custom_roi_type,
                IfNull(lp.custom_base_rate,'') AS custom_base_rate,
                IfNull(lp.custom_minimum_days_for_1st_repayment_date,'') AS custom_minimum_days_for_1st_repayment_date,
                IfNull(lp.custom_maximum_days_for_1st_repayment_date,'') AS custom_maximum_days_for_1st_repayment_date,
                IfNull(lp.custom_mutitranche_allowed,'') AS custom_mutitranche_allowed,
                IfNull(lp.custom_sub_standard_definition_for_collection_offset_logic,'') AS custom_sub_standard_definition_for_collection_offset_logic,
                IfNull(lp.custom_dpd_threshold_for_sub_standard_definition,'') AS custom_dpd_threshold_for_sub_standard_definition,
                IfNull(lp.custom_standard_knockoff_sequence,'') AS custom_standard_knockoff_sequence,
                IfNull(lp.custom_npa_knockoff_sequence,'') AS custom_npa_knockoff_sequence,
                IfNull(lp.custom_write_off__knockoff_sequence,'') AS custom_write_off__knockoff_sequence,
                IfNull(lp.custom_minimum_loan_amount,'') AS custom_minimum_loan_amount,
                IfNull(lp.custom_default_loan_amount,'') AS custom_default_loan_amount,
                IfNull(lp.custom_minimum_spread_rate,'') AS custom_minimum_spread_rate,
                IfNull(lp.custom_maximum_spread_rate,'') AS custom_maximum_spread_rate,
                IfNull(lp.custom_minimum_rate_of_interest,'') AS custom_minimum_rate_of_interest,
                IfNull(lp.custom_maximum_rate_of_interest,'') AS custom_maximum_rate_of_interest,
                IfNull(lp.custom_interest_treatment_after_moratorium_period,'') AS custom_interest_treatment_after_moratorium_period,
                IfNull(lp.custom_is_bill_discounting_product,'') AS custom_is_bill_discounting_product
            FROM `tabLoan Product` lp
            WHERE lp.name = %(product)s

        """, values=values, as_dict=1)
        if data1:
            data.update(data1[0])
        
        return data
