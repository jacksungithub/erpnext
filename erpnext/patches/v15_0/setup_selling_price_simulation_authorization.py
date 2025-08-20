import frappe


def execute():
	"""Setup authorization rules for Selling Price Simulation"""
	
	if not frappe.db.exists("Authorization Rule", {"transaction": "Selling Price Simulation", "based_on": "Grand Total"}):
		auth_rule = frappe.get_doc({
			"doctype": "Authorization Rule",
			"transaction": "Selling Price Simulation",
			"based_on": "Grand Total",
			"system_role": "Sales Manager",
			"approving_role": "Sales Manager",
			"value": 0,
			"company": "",
			"applicable_for": "All"
		})
		auth_rule.insert(ignore_permissions=True)
		
	if not frappe.db.exists("Authorization Rule", {"transaction": "Selling Price Simulation", "based_on": "Grand Total", "value": 10000}):
		auth_rule = frappe.get_doc({
			"doctype": "Authorization Rule", 
			"transaction": "Selling Price Simulation",
			"based_on": "Grand Total",
			"system_role": "Sales Manager",
			"approving_role": "System Manager",
			"value": 10000,
			"company": "",
			"applicable_for": "All"
		})
		auth_rule.insert(ignore_permissions=True)
