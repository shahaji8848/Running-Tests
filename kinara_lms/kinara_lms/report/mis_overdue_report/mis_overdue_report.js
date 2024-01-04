// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.query_reports["MIS Overdue Report"] = {
	"filters": [
		{
			"fieldname":"date",
			"label": __("Date"),
			"fieldtype": "Date",
			"reqd": 1
		},
		{
			"fieldname":"hub",
			"label": __("Hub"),
			"fieldtype": "Link",
			"options": "Branch"
		}
	]
};
