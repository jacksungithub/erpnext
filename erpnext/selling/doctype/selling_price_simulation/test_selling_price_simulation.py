
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import flt


class TestSellingPriceSimulation(FrappeTestCase):
	def setUp(self):
		if not frappe.db.exists("Item", "TEST-COMPONENT-001"):
			item = frappe.get_doc({
				"doctype": "Item",
				"item_code": "TEST-COMPONENT-001",
				"item_name": "Test Electronic Component",
				"item_group": "All Item Groups",
				"stock_uom": "Nos",
				"is_stock_item": 1
			})
			item.insert()
			
		for i in range(1, 4):
			supplier_name = f"Test Supplier {i}"
			if not frappe.db.exists("Supplier", supplier_name):
				supplier = frappe.get_doc({
					"doctype": "Supplier",
					"supplier_name": supplier_name,
					"supplier_group": "All Supplier Groups"
				})
				supplier.insert()
				
	def test_cost_analysis_calculation(self):
		sps = frappe.get_doc({
			"doctype": "Selling Price Simulation",
			"item_code": "TEST-COMPONENT-001",
			"company": "_Test Company",
			"currency": "USD",
			"supplier_offers": [
				{
					"supplier": "Test Supplier 1",
					"price_usd": 10.00,
					"quotation_reference": "QTN-001"
				},
				{
					"supplier": "Test Supplier 2", 
					"price_usd": 12.00,
					"quotation_reference": "QTN-002"
				},
				{
					"supplier": "Test Supplier 3",
					"price_usd": 8.00,
					"quotation_reference": "QTN-003"
				}
			]
		})
		sps.insert()
		
		self.assertEqual(flt(sps.lowest_cost), 8.00)
		self.assertEqual(flt(sps.average_cost), 10.00)
		self.assertEqual(flt(sps.maximum_cost), 12.00)
		
	def test_suggested_selling_price_calculation(self):
		sps = frappe.get_doc({
			"doctype": "Selling Price Simulation",
			"item_code": "TEST-COMPONENT-001",
			"company": "_Test Company",
			"currency": "USD",
			"market_price": 100.00,
			"customer_target_price": 90.00,
			"supplier_offers": [
				{
					"supplier": "Test Supplier 1",
					"price_usd": 10.00,
					"quotation_reference": "QTN-001"
				}
			]
		})
		sps.insert()
		
		self.assertGreater(flt(sps.suggested_selling_price), 0)
		self.assertGreater(flt(sps.china_selling_price_cny), 0)
		self.assertGreater(flt(sps.gross_profit_margin), 0)
		
	def test_approval_workflow(self):
		sps = frappe.get_doc({
			"doctype": "Selling Price Simulation",
			"item_code": "TEST-COMPONENT-001",
			"company": "_Test Company",
			"currency": "USD",
			"supplier_offers": [
				{
					"supplier": "Test Supplier 1",
					"price_usd": 10.00,
					"quotation_reference": "QTN-001"
				}
			]
		})
		sps.insert()
		
		self.assertEqual(sps.status, "Draft")
		
		sps.submit_for_approval()
		self.assertEqual(sps.status, "Pending Approval")
		
		sps.approve_simulation()
		self.assertEqual(sps.status, "Approved")
		self.assertIsNotNone(sps.approved_by)
		self.assertIsNotNone(sps.approval_date)
