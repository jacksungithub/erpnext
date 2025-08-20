import frappe
from frappe import _


def setup_test_data():
	"""Setup test data for selling price simulation"""
	
	companies = [
		{
			"company_name": "Hong Kong Electronics Ltd",
			"abbr": "HKE",
			"default_currency": "USD",
			"country": "Hong Kong"
		},
		{
			"company_name": "China Electronics Co Ltd", 
			"abbr": "CEC",
			"default_currency": "CNY",
			"country": "China"
		}
	]
	
	for company_data in companies:
		if not frappe.db.exists("Company", company_data["company_name"]):
			company = frappe.get_doc({
				"doctype": "Company",
				**company_data
			})
			company.insert(ignore_permissions=True)
			
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
		
	test_items = [
		{
			"item_code": "ELEC-COMP-001",
			"item_name": "Electronic Component - Resistor 10K",
			"description": "10K Ohm Resistor for electronic circuits"
		},
		{
			"item_code": "ELEC-COMP-002", 
			"item_name": "Electronic Component - Capacitor 100uF",
			"description": "100 microFarad electrolytic capacitor"
		},
		{
			"item_code": "ELEC-COMP-003",
			"item_name": "Electronic Component - LED Red 5mm",
			"description": "Red LED 5mm diameter for indicators"
		}
	]
	
	for item_data in test_items:
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
			
	test_suppliers = [
		"Overseas Electronics Ltd",
		"Global Components Inc", 
		"Asia Pacific Electronics",
		"European Tech Supplies",
		"American Electronic Parts"
	]
	
	for supplier_name in test_suppliers:
		if not frappe.db.exists("Supplier", supplier_name):
			supplier = frappe.get_doc({
				"doctype": "Supplier",
				"supplier_name": supplier_name,
				"supplier_group": "All Supplier Groups"
			})
			supplier.insert(ignore_permissions=True)
			
	if not frappe.db.exists("Selling Price Simulation", {"item_code": "ELEC-COMP-001"}):
		sps = frappe.get_doc({
			"doctype": "Selling Price Simulation",
			"item_code": "ELEC-COMP-001",
			"company": "Hong Kong Electronics Ltd",
			"currency": "USD",
			"market_price": 15.00,
			"customer_target_price": 12.00,
			"supplier_offers": [
				{
					"supplier": "Overseas Electronics Ltd",
					"price_usd": 8.50,
					"quotation_reference": "OEL-QTN-001",
					"lead_time_days": 14,
					"remarks": "Bulk pricing available"
				},
				{
					"supplier": "Global Components Inc",
					"price_usd": 9.20,
					"quotation_reference": "GCI-QTN-002", 
					"lead_time_days": 10,
					"remarks": "Express shipping available"
				},
				{
					"supplier": "Asia Pacific Electronics",
					"price_usd": 7.80,
					"quotation_reference": "APE-QTN-003",
					"lead_time_days": 21,
					"remarks": "Best price but longer lead time"
				}
			]
		})
		sps.insert(ignore_permissions=True)
		
	frappe.db.commit()
	return _("Test data setup completed successfully!")


@frappe.whitelist()
def create_sample_simulation():
	"""Create a sample selling price simulation for testing"""
	return setup_test_data()
