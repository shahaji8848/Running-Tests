// Copyright (c) 2024, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.query_reports["Disbursement Report"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"partner_name",
			"label": __("Partner Name"),
			"fieldtype": "Link",
			"options": "Loan Partner"
		}
	]
};
