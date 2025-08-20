from frappe import _


def get_data():
	return {
		"fieldname": "selling_price_simulation",
		"non_standard_fieldnames": {
			"Quotation": "selling_price_simulation"
		},
		"transactions": [
			{
				"label": _("Sales"),
				"items": ["Quotation"]
			}
		]
	}
