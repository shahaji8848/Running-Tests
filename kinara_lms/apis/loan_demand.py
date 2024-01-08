import frappe
import json


@frappe.whitelist()
def get_demand_data(**kwargs):
    date = kwargs["date"]
    type = kwargs["type"]
    conditions = [
                    f"demand.demand_type = 'EMI'", 
                    f"demand.docstatus = 1"
                ]
    subquery_conditions = [
                        f"ld.demand_type = 'EMI'", 
                        f"ld.docstatus = 1"
                    ]
    order_by = ""
    if type == "scheduled":
        conditions.append(f"demand.demand_date = '{date}'")
        subquery_conditions.append(f"ld.demand_date = '{date}'")
    elif type == "overdue":
        conditions.append(f"demand.demand_date <= '{date}' ")
        subquery_conditions.append(f"ld.demand_date <= '{date}'")
        order_by = "ORDER BY installment_details.payment_date DESC"
    else:
        return {"error": "invalid type value "+type}
    
    where_clause = "WHERE " + " AND ".join(conditions)
    subquery_where_clause = "WHERE " + " AND ".join(subquery_conditions)

    demands_details  = frappe.db.sql(f"""
                                        SELECT COALESCE(NULLIF(co_lending_partner.partner_name,''), NULLIF(loan_channel_partner.name1,''), loan.company) as "partner_name",
                                            loan.sponsor_bank_code as "Sponsor Bank Code", 
                                            loan.hub as "Hub", 
                                            loan.name as "AccountID", 
                                            loan.applicant as "ClientID", 
                                            loan_product.product_name as "ProductName",
                                            entity.customer_name as "ClientName", 
                                            applicant.customer_name as "Proprietor Name", 
                                            loan.loan_amount as "LoanAmount", SUM(demand.demand_amount - demand.paid_amount) as "Current Due", 
                                            loan_repayment.repayment_mode as "Repayment Mode", 
                                            demand_details.name as "Demand Name",
                                            demand_details.realization_status as "Realization Status", 
                                            demand_details.realization_reason as "Realization Reason", 
                                            demand_details.realization_date as "Realization Date",
                                            installment_details.payment_date as "InstallmentDueDate", 
                                            installment_details.idx as "NoOfInstallment", 
                                            loan_repayment_schedule.repayment_periods as "Term",
                                            entity.mobile_no as "Mobile No" 
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
                                            {where_clause}
                                            GROUP BY loan.name
                                            {order_by}""", as_dict=1)
    
    response = []
    for demand_detail in demands_details:
        response_doc = {
            "partner_name" : demand_detail["partner_name"],
            "Sponsor Bank Code": demand_detail["Sponsor Bank Code"],
            "Hub": demand_detail["Hub"],
            "Spoke": None,
            "ClientID": demand_detail["ClientID"],
            "AccountID": demand_detail["AccountID"],
            "ProductName": demand_detail["ProductName"],
            "ClientName": demand_detail["ClientName"],
            "Proprietor Name": demand_detail["Proprietor Name"],
            "InstallmentDueDate": demand_detail["InstallmentDueDate"],
            "LoanAmount": demand_detail["LoanAmount"],
            "Cheque ID": None,
            "Current Due": demand_detail["Current Due"],
            "NoOfInstallment": demand_detail["NoOfInstallment"],
            "Term": demand_detail["Term"],
            "Repayment Mode": demand_detail["Repayment Mode"],
            "Bank Name": None,
            "Branch Name": None,
            # "Demand Name": demand_detail["Demand Name"],
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
    return response

@frappe.whitelist()
def update_bulk_loan_demand(**kwargs):
    allowed_fields = ["realization_status","realization_reason","realization_date"]
    response = {
		"data": []
    }
    body = json.loads(frappe.request.data)
    for data in body["data"]:
        response_dict = {
			"status" : "",
		}
        try:
            if "name" not in data:
                frappe.throw("Record Name Is Mandatory")
            doc = frappe.get_doc("Loan Demand",data["name"])
            for key in data.keys():
                if key in allowed_fields:
                    doc.set(key, data[key])
            doc.save()
            response_dict["name"] = doc.name
            response_dict["status"] = "success"
            response_dict["message"] = "record updated"
            response_dict["doc"] = doc
        except Exception as e:
            response_dict["status"] = "error"
            response_dict["message"] = e
        response["data"].append(response_dict)
    return response