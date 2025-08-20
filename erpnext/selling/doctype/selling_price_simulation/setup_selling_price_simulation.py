import frappe
from frappe import _


def setup_selling_price_simulation():
	"""Setup function to configure selling price simulation"""
	
	if not frappe.db.exists("Company", "Hong Kong Electronics Ltd"):
		hk_company = frappe.get_doc({
			"doctype": "Company",
			"company_name": "Hong Kong Electronics Ltd",
			"abbr": "HKE",
			"default_currency": "USD",
			"country": "Hong Kong"
		})
		hk_company.insert(ignore_permissions=True)
		
	if not frappe.db.exists("Company", "China Electronics Co Ltd"):
		china_company = frappe.get_doc({
			"doctype": "Company", 
			"company_name": "China Electronics Co Ltd",
			"abbr": "CEC",
			"default_currency": "CNY",
			"country": "China"
		})
		china_company.insert(ignore_permissions=True)
		
	if not frappe.db.exists("Currency Exchange", {"from_currency": "USD", "to_currency": "CNY"}):
		exchange_rate = frappe.get_doc({
			"doctype": "Currency Exchange",
			"from_currency": "USD",
			"to_currency": "CNY", 
			"exchange_rate": 7.2,
			"for_buying": 1,
			"for_selling": 1
		})
		exchange_rate.insert(ignore_permissions=True)
		
	sample_items = [
		{
			"item_code": "ELEC-COMP-001",
			"item_name": "Electronic Component - Resistor 10K",
			"description": "10K Ohm Resistor for electronic circuits"
		},
		{
			"item_code": "ELEC-COMP-002", 
			"item_name": "Electronic Component - Capacitor 100uF",
			"description": "100 microFarad electrolytic capacitor"
		}
	]
	
	for item_data in sample_items:
		if not frappe.db.exists("Item", item_data["item_code"]):
			item = frappe.get_doc({
				"doctype": "Item",
				"item_code": item_data["item_code"],
				"item_name": item_data["item_name"],
				"item_group": "All Item Groups",
				"stock_uom": "Nos",
				"is_stock_item": 1,
				"description": item_data["description"]
			})
			item.insert(ignore_permissions=True)
			
	sample_suppliers = [
		"Overseas Electronics Ltd",
		"Global Components Inc", 
		"Asia Pacific Electronics"
	]
	
	for supplier_name in sample_suppliers:
		if not frappe.db.exists("Supplier", supplier_name):
			supplier = frappe.get_doc({
				"doctype": "Supplier",
				"supplier_name": supplier_name,
				"supplier_group": "All Supplier Groups"
			})
			supplier.insert(ignore_permissions=True)
			
	frappe.db.commit()
	return _("Selling Price Simulation setup completed successfully!")
