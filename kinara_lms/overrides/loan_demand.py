import frappe
from frappe import _
import datetime
from frappe.permissions.perm_manager import update_permission



def after_submit(doc, method=None):
	generate_bill_of_supply(doc)

def generate_bill_of_supply(doc, method=None):
        if doc.demand_type == "EMI":
            bs_exist = frappe.db.get_list('Bill of Supply',filters={'repayment_schedule_detail': doc.repayment_schedule_detail, 'docstatus':1})

        if doc.demand_type == "Charges":
            bs_exist = frappe.db.get_list('Bill of Supply',filters={'loan_demand_detail': doc.name, 'docstatus':1})
            
        if len(bs_exist) == 0:
            bs_doc = frappe.new_doc('Bill of Supply')
            bs_doc.ti_number = doc.sales_invoice
            bs_doc.loan_id = doc.loan
            bs_doc.loan_installment_date = doc.demand_date
            bs_doc.loan_demand_detail = doc.name
            bs_doc.posting_date = datetime.datetime.now().date()
            if doc.demand_type == "EMI":
                bs_doc.repayment_schedule_detail = doc.repayment_schedule_detail
                try:
                    rs = frappe.get_doc('Repayment Schedule', doc.repayment_schedule_detail)
                    principal = rs.principal_amount
                    interest = rs.interest_amount
                except:
                    principal, interest = 0,0
                bs_doc.append('items',{'particulars':"Principal Amount",'amount':principal})
                bs_doc.append('items',{'particulars':"Interest Amount",'amount':interest})
            if doc.demand_type == "Charges":
                charges = doc.demand_amount - doc.paid_amount
                bs_doc.append('items',{'particulars':"Charges Amount",'amount':charges})
            bs_doc.save()
            bs_doc.submit()