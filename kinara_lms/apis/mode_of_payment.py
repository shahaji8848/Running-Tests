import frappe

@frappe.whitelist()
def get_mod_details(mod):
    
    if frappe.db.exists('Mode of Payment',mod):
        return mod_details(mod)
    else:
        return no_mod_details()

def mod_details(mod):
    values = {'mod': mod}
    if frappe.db.exists('Mode of Payment Account',{'parent':mod}):
        data = frappe.db.sql("""
            SELECT
                mop.name as name,
                mop.enabled as enabled,
                mop.type as type,
                mopa.company as company,
                mopa.default_account as default_account
                
            FROM `tabMode of Payment` mop
            JOIN `tabMode of Payment Account` mopa
            ON mop.name = mopa.parent
            WHERE mop.name = %(mod)s
        """, values=values, as_dict=1)
        return data
    else:
        data = frappe.db.sql("""
            SELECT
                mop.name as name,
                mop.enabled as enabled,
                mop.type as type
            FROM `tabMode of Payment` mop
            WHERE mop.name = %(mod)s
        """, values=values, as_dict=1)
        return data

def no_mod_details():
    data1 = frappe.db.sql("""
        SELECT
            mop.name as name,
            mop.enabled as enabled,
            mop.type as type,
            CASE
                WHEN mop.name = mopa.parent THEN mopa.company
                ELSE ''
            END AS company,
            CASE
                WHEN mop.name = mopa.parent THEN mopa.default_account
                ELSE ''
            END AS default_account
            
        FROM `tabMode of Payment` mop
        JOIN `tabMode of Payment Account` mopa
        
    """,  as_dict=1)
    return data1
