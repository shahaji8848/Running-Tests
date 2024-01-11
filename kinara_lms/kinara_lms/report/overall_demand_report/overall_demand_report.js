// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.query_reports["Overall demand Report"] = {
	"filters": [
		{
			"fieldname": "report_type",
			"fieldtype": "Select",
			"label": "Report Type",
			"options": "\nScheduled\nOverdue",
			"default": "Scheduled",
		},
		{
            "fieldname":"from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "80",
        },
        {
            "fieldname":"to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "80",
        }
	]
};
