import frappe


@frappe.whitelist()
def get_demand_data(**kwargs):
    date = kwargs["date"]
    if kwargs["type"] == "scheduled":
        where_clause = f"WHERE demand.demand_type = 'EMI' AND demand.demand_date = '{date}' "
        repayment_schedule_and_latest_loan_demand_wc = f"WHERE ld.demand_type = 'EMI' AND ld.demand_date = '{date}' "
    elif kwargs["type"] == "overdue":
        where_clause = f"WHERE demand.demand_date <= '{date}' "
        repayment_schedule_and_latest_loan_demand_wc = f"WHERE ld.demand_type = 'EMI' AND ld.demand_date <= '{date}' "
    else:
        return {"error": "invalid type value "+kwargs["type"]}

        
    # repayment_schedule_and_latest_loan_demand  = frappe.db.sql(f"""
    #                                                             SELECT ld.name as "Loan Demand", rs.name as "Repayment Schedule"
    #                                                             FROM `tabRepayment Schedule` as rs
    #                                                             JOIN `tabLoan Demand` as ld ON ld.repayment_schedule_detail = rs.name
    #                                                             {repayment_schedule_and_latest_loan_demand_wc}
    #                                                             ORDER BY ld.demand_date DESC, ld.modified DESC
    #                                                             LIMIT 1""", as_dict=1)
    
    # demand_repayment_schedule = repayment_schedule_and_latest_loan_demand[0]['Repayment Schedule']
    # latest_demand_name = repayment_schedule_and_latest_loan_demand[0]['Loan Demand']    
    demands_details  = frappe.db.sql(f"""
                                        SELECT COALESCE(NULLIF(loan.co_lending_partner,''), NULLIF(loan.custom_channel_partner,''), loan.company) as "partner_name", 
                                            loan.sponsor_bank_code as "Sponsor Bank Code", 
                                            loan.hub as "Hub", 
                                            loan.name as "AccountID", 
                                            loan.applicant as "ClientID", 
                                            loan_product.product_name as "ProductName",
                                            entity.customer_name as "ClientName", 
                                            applicant.customer_name as "Proprietor Name", 

                                            loan.loan_amount as "LoanAmount", SUM(demand.demand_amount - demand.paid_amount) as "Current Due", 
                                            
                                            loan_repayment.repayment_mode as "Repayment Mode", 
                                            
                                            entity.mobile_no as "Mobile No" 
                                        FROM `tabLoan Demand` as demand
                                            LEFT JOIN `tabLoan` as loan ON demand.loan = loan.name
                                            LEFT JOIN `tabLoan Repayment` as loan_repayment ON loan_repayment.against_loan = loan.name
                                            LEFT JOIN `tabCustomer` as entity ON entity.name = loan.applicant
                                            LEFT JOIN `tabCustomer` as applicant ON applicant.name = loan.custom_individual_applicant
                                            LEFT JOIN `tabLoan Product` as loan_product ON loan_product.name = loan.loan_product
                                        {where_clause}
                                        GROUP BY loan.name""", as_dict=1)
    
    # installment_details.payment_date as "InstallmentDueDate", 
    
    # installment_details.idx as "NoOfInstallment", 
                                            # loan_repayment_schedule.repayment_periods as "Term",
    
    # realization_details.realization_status as "Realization Status", 
                                            # realization_details.realization_reason as "Realization Reason", 
                                            # realization_details.realization_date as "Realization Date", 
    

    # LEFT JOIN `tabRepayment Schedule` as installment_details ON installment_details.name = '{demand_repayment_schedule}'
                                            # LEFT JOIN `tabLoan Repayment Schedule` as loan_repayment_schedule ON loan_repayment_schedule.name = installment_details.parent
                                            # LEFT JOIN `tabLoan Demand` as realization_details ON realization_details.name = '{latest_demand_name}'
    response = []
    for demand_detail in demands_details:
        response_doc = {
            "partner_name" : demand_detail["partner_name"],
            "Sponsor Bank Code": demand_detail["Sponsor Bank Code"],
            "Hub": demand_detail["Hub"],
            "Spoke": demand_detail["Spoke"],
            "ClientID": demand_detail["ClientID"],
            "AccountID": demand_detail["AccountID"],
            "ProductName": demand_detail["ProductName"],
            "ClientName": demand_detail["ClientName"],
            "Proprietor Name": demand_detail["Proprietor Name"],
            # "InstallmentDueDate": demand_detail["InstallmentDueDate"],
            "LoanAmount": demand_detail["LoanAmount"],
            # "Cheque ID": demand_detail["Cheque ID"],
            "Current Due": demand_detail["Current Due"],
            # "NoOfInstallment": demand_detail["NoOfInstallment"],
            # "Term": demand_detail["Term"],
            "Repayment Mode": demand_detail["Repayment Mode"],
            # "Bank Name": demand_detail["Bank Name"],
            # "Branch Name": demand_detail["Branch Name"],
            # "Realization Status": demand_detail["Realization Status"],
            # "Realization Reason": demand_detail["Realization Reason"],
            # "Realization Date": demand_detail["Realization Date"],
            "Mobile No.": demand_detail["Mobile No"],
        }
        response.append(response_doc)
        # repayment_schedule_and_latest_loan_demand_wc += f" AND ld.loan = '{response_doc['AccountID']}'"
        repayment_schedule_and_latest_loan_demand  = frappe.db.sql(f"""
                                                                SELECT ld.name as "Loan Demand", rs.name as "Repayment Schedule"
                                                                FROM `tabRepayment Schedule` as rs
                                                                JOIN `tabLoan Demand` as ld ON ld.repayment_schedule_detail = rs.name
                                                                {repayment_schedule_and_latest_loan_demand_wc}
                                                                ORDER BY ld.demand_date DESC, ld.modified DESC
                                                                LIMIT 1""", as_dict=1)
        if len(repayment_schedule_and_latest_loan_demand) > 0:
            repayment_schedule = repayment_schedule_and_latest_loan_demand[0]["Repayment Schedule"]
            loan_demand = repayment_schedule_and_latest_loan_demand[0]["Loan Demand"]
            realization_details = frappe.db.sql(f"""
                                 SELECT realization.bank_name as "Bank Name", ach.branch_name as "Branch Name"
                                 FROM `tabLoan ACH` as ach
                                    WHERE ach.loan = '{demand_detail["AccountID"]}'
                                ach.docstatus = 1
                             ORDER BY ach.modified DESC
                                 LIMIT 1""", as_dict=1)

        # repayment_
        # realization_details = frappe.db.sql(f"""
        #                         SELECT ach.bank_name as "Bank Name", ach.branch_name as "Branch Name"
        #                         FROM `tabLoan ACH` as ach
        #                         WHERE ach.loan = '{demand_detail["AccountID"]}'
        #                         ach.docstatus = 1
        #                         ORDER BY ach.modified DESC
        #                         LIMIT 1""", as_dict=1)
        # if demand_detail["Repayment Mode"] == "ACH":
        #     ach = frappe.db.sql(f"""
        #                         SELECT ach.bank_name as "Bank Name", ach.branch_name as "Branch Name"
        #                         FROM `tabLoan ACH` as ach
        #                         WHERE ach.loan = '{demand_detail["AccountID"]}'
        #                         ach.docstatus = 1
        #                         ORDER BY ach.modified DESC
        #                         LIMIT 1""", as_dict=1)
        #     if len(ach) > 0:
        #         response_doc["Bank Name"] = ach[0]["Bank Name"]
        #         response_doc["Branch Name"] = ach[0]["Branch Name"]
        # if demand_detail["Repayment Mode"] == "PDC":
        #     ach = frappe.db.sql(f"""
        #                         SELECT pdc.bank_name as "Bank Name", pdc.branch_name as "Branch Name"
        #                         FROM `tabLoan PDC` as pdc
        #                         WHERE pdc.loan = '{demand_detail["AccountID"]}'
        #                         AND pdc.emi = '{demand_detail["AccountID"]}'
        #                         pdc.status = "Active"
        #                         ORDER BY pdc.modified DESC
        #                         LIMIT 1""", as_dict=1)
        #     if len(ach) > 0:
        #         response_doc["Bank Name"] = ach[0]["Bank Name"]
        #         response_doc["Branch Name"] = ach[0]["Branch Name"]
        


    
    # demands_current_due_and_other_details  = frappe.db.sql(f"""
    #         SELECT loan.co_lending_partner as "partner_name", 
    #             loan.sponsor_bank_code as "Sponsor Bank Code",
    #             loan.hub as "Hub", 
    #             loan.name as "AccountID", 
    #             loan.applicant as "ClienctID", 
    #             loan_product.product_name,
    #             entity.customer_name as "ClientName", 
    #             applicant.customer_name as "Proprietor Name", 
    #             loan.loan_amount as "LoanAmount",
    #             SUM(demand.demand_amount - demand.paid_amount) as "Current Due", 
    #             entity.mobile_no as "Mobile No" 
    #         FROM `tabLoan Demand` as demand
    #         JOIN `tabLoan` as loan
    #             ON demand.loan = loan.name
    #         JOIN `tabLoan Repayment` as loan_repayment
    #             ON loan_repayment.against_loan = loan.name
    #         JOIN `tabCustomer` as entity
    #             ON entity.name = loan.applicant
    #         JOIN `tabCustomer` as applicant
    #             ON applicant.name = loan.custom_individual_applicant
    #         JOIN `tabLoan Product` as loan_product
    #             ON loan_product.name = loan.loan_product
    #         {where_clause}
    #         GROUP BY loan.name""", as_dict=1)
