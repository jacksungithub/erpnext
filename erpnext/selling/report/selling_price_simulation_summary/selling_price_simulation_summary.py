# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{
			"label": _("Simulation ID"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Selling Price Simulation",
			"width": 150
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 120
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 150
		},
		{
			"label": _("Company"),
			"fieldname": "company",
			"fieldtype": "Link",
			"options": "Company",
			"width": 120
		},
		{
			"label": _("Status"),
			"fieldname": "status",
			"fieldtype": "Data",
			"width": 100
		},
		{
			"label": _("Lowest Cost"),
			"fieldname": "lowest_cost",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Average Cost"),
			"fieldname": "average_cost",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Maximum Cost"),
			"fieldname": "maximum_cost",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Market Price"),
			"fieldname": "market_price",
			"fieldtype": "Currency",
			"width": 100
		},
		{
			"label": _("Suggested Selling Price"),
			"fieldname": "suggested_selling_price",
			"fieldtype": "Currency",
			"width": 150
		},
		{
			"label": _("Gross Profit Margin (%)"),
			"fieldname": "gross_profit_margin",
			"fieldtype": "Percent",
			"width": 120
		},
		{
			"label": _("Approved By"),
			"fieldname": "approved_by",
			"fieldtype": "Link",
			"options": "User",
			"width": 120
		}
	]


def get_data(filters):
	conditions = []
	values = []
	
	if filters.get("company"):
		conditions.append("company = %s")
		values.append(filters.get("company"))
		
	if filters.get("status"):
		conditions.append("status = %s")
		values.append(filters.get("status"))
		
	if filters.get("item_code"):
		conditions.append("item_code = %s")
		values.append(filters.get("item_code"))
		
	where_clause = ""
	if conditions:
		where_clause = "WHERE " + " AND ".join(conditions)
		
	query = f"""
		SELECT 
			name, item_code, item_name, company, status,
			lowest_cost, average_cost, maximum_cost, market_price,
			suggested_selling_price, gross_profit_margin, approved_by
		FROM `tabSelling Price Simulation`
		{where_clause}
		ORDER BY modified DESC
	"""
	
	return frappe.db.sql(query, values, as_dict=1)
