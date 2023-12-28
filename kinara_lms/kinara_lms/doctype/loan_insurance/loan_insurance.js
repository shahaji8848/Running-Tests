// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.ui.form.on('Loan Insurance', {
	nominee_urn: function(frm) {
		if(frm.doc.nominee_urn){
		    frappe.db.get_value('Customer',frm.doc.nominee_urn,'customer_name', (customer) => {
			    if (customer.hasOwnProperty("customer_name")) {
				    frm.set_value("nominee_name", customer.customer_name)
			    }
                else{
                    frm.set_value("nominee_name", null)
                }
		})
	}
	},

});