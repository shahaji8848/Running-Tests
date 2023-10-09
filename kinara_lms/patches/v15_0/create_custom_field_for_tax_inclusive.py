from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
	create_custom_fields(
		{
			"Item": [
				{
					"default": "0",
					"fieldname": "tax_inclusive",
					"label": "Tax Inclusive",
					"fieldtype": "Check",
					"insert_after": "stock_uom",
				},
			],
		},
		ignore_validate=True,
	)
