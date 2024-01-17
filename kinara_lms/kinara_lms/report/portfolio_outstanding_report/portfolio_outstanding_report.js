// Copyright (c) 2024, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.query_reports["Portfolio Outstanding Report"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
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
