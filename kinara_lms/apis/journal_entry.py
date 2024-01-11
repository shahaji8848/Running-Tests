import frappe


@frappe.whitelist()
def last_jv_entry_for_the_loan(**kwargs):
    loan = kwargs["loan"]
    last_je = frappe.db.sql(f"""SELECT je.name, je.posting_date
                                    FROM `tabJournal Entry` as je
                                    JOIN `tabJournal Entry Account` as jea ON je.name = jea.parent
                                    WHERE jea.reference_type = "Loan"
                                    AND jea.reference_name = "{loan}"
                                    AND je.docstatus = 1
                                    ORDER BY je.posting_date DESC, je.modified DESC
                                    LIMIT 1
								""")
    last_je_date = last_je[0][1]
    last_restructure_for_a_loan = frappe.db.sql(f"""SELECT lr.restructure_date
                                    FROM `tabLoan Restructure` as lr
                                    WHERE lr.loan = "{loan}"
                                    AND lr.docstatus = 1
                                    ORDER BY lr.restructure_date DESC, je.modified DESC
                                    LIMIT 1
								    """)
    last_restructure_date = last_restructure_for_a_loan[0][0]
    if last_restructure_date > last_je_date:
        return {"error": "Loan Restructure after the Transaction Date"}
    else:
        doc = frappe.get_doc('Journal Entry', last_je[0][0])
        return {"Last JV Entry": doc}

    