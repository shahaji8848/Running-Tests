from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Loan Partner": [
				{
					"fieldname": "processing_fee_billing",
					"label": "Processing Fee Billing (against partner share)",
					"fieldtype": "Percent",
					"insert_after": "servicer_fee",
				},
			],
		},
		ignore_validate=True,
	)
