# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from frappe.utils import flt, getdate, nowdate
from erpnext.setup.utils import get_exchange_rate


class SellingPriceSimulation(Document):
	def validate(self):
		self.calculate_cost_analysis()
		self.calculate_suggested_selling_price()
		self.set_currency_and_conversion_rate()
		
	def before_submit(self):
		if self.status != "Approved":
			frappe.throw(_("Only approved selling price simulations can be submitted"))
			
	def on_submit(self):
		self.validate_approval_authority()
		
	def set_currency_and_conversion_rate(self):
		if self.company and not self.currency:
			self.currency = frappe.get_cached_value("Company", self.company, "default_currency")
			
		if self.currency and not self.conversion_rate:
			company_currency = frappe.get_cached_value("Company", self.company, "default_currency")
			if self.currency != company_currency:
				self.conversion_rate = get_exchange_rate(self.currency, company_currency, getdate())
			else:
				self.conversion_rate = 1.0
				
	def calculate_cost_analysis(self):
		if not self.supplier_offers:
			return
			
		prices = []
		for offer in self.supplier_offers:
			if offer.price_usd:
				prices.append(flt(offer.price_usd))
				
		if prices:
			self.lowest_cost = min(prices)
			self.average_cost = sum(prices) / len(prices)
			self.maximum_cost = max(prices)
			self.hk_company_cost_usd = self.lowest_cost
			
	def calculate_suggested_selling_price(self):
		if not self.lowest_cost:
			return
			
		try:
			conversion_rate = get_exchange_rate("USD", "CNY", getdate())
		except:
			conversion_rate = 7.2  # Default fallback rate
			
		cost_cny = flt(self.lowest_cost) * flt(conversion_rate)
		
		vat_rate = flt(self.china_vat_rate) / 100 if self.china_vat_rate else 0.13
		cost_with_vat = cost_cny * (1 + vat_rate)
		
		base_price = cost_with_vat
		
		if self.market_price and self.customer_target_price:
			price_ceiling = min(flt(self.market_price), flt(self.customer_target_price))
			if price_ceiling > base_price:
				self.suggested_selling_price = base_price + (price_ceiling - base_price) * 0.8
			else:
				self.suggested_selling_price = base_price * 1.1  # Minimal margin
		elif self.market_price:
			if flt(self.market_price) > base_price:
				self.suggested_selling_price = base_price + (flt(self.market_price) - base_price) * 0.7
			else:
				self.suggested_selling_price = base_price * 1.05
		elif self.customer_target_price:
			if flt(self.customer_target_price) > base_price:
				self.suggested_selling_price = min(flt(self.customer_target_price), base_price * 1.25)
			else:
				self.suggested_selling_price = base_price * 1.05
		else:
			self.suggested_selling_price = base_price * 1.20
			
		self.china_selling_price_cny = self.suggested_selling_price
		
		if self.suggested_selling_price and cost_cny:
			self.gross_profit_margin = ((self.suggested_selling_price - cost_cny) / self.suggested_selling_price) * 100
			
	def validate_approval_authority(self):
		if self.status == "Pending Approval":
			auth_control = frappe.get_doc("Authorization Control")
			auth_control.validate_approving_authority(
				"Selling Price Simulation", 
				self.company, 
				flt(self.suggested_selling_price),
				self
			)
			
	@frappe.whitelist()
	def submit_for_approval(self):
		if self.status != "Draft":
			frappe.throw(_("Only draft simulations can be submitted for approval"))
			
		if not self.supplier_offers:
			frappe.throw(_("Please add at least one supplier offer"))
			
		self.status = "Pending Approval"
		self.save()
		frappe.msgprint(_("Selling Price Simulation submitted for approval"))
		
	@frappe.whitelist()
	def approve_simulation(self):
		if not frappe.has_permission(self.doctype, "write"):
			frappe.throw(_("Not permitted to approve"))
			
		if self.status != "Pending Approval":
			frappe.throw(_("Only pending simulations can be approved"))
			
		self.status = "Approved"
		self.approved_by = frappe.session.user
		self.approval_date = nowdate()
		self.save()
		frappe.msgprint(_("Selling Price Simulation approved"))
		
	@frappe.whitelist()
	def reject_simulation(self):
		if not frappe.has_permission(self.doctype, "write"):
			frappe.throw(_("Not permitted to reject"))
			
		if self.status != "Pending Approval":
			frappe.throw(_("Only pending simulations can be rejected"))
			
		self.status = "Rejected"
		self.save()
		frappe.msgprint(_("Selling Price Simulation rejected"))


@frappe.whitelist()
def make_quotation(source_name, target_doc=None):
	def set_missing_values(source, target):
		target.quotation_to = "Customer"
		target.selling_price_list = frappe.db.get_single_value("Selling Settings", "selling_price_list")
		target.run_method("set_missing_values")
		target.run_method("calculate_taxes_and_totals")
		
	def update_item(obj, target, source_parent):
		target.item_code = source_parent.item_code
		target.item_name = source_parent.item_name
		target.description = source_parent.description
		target.qty = 1
		target.rate = source_parent.suggested_selling_price
		target.amount = target.rate * target.qty
		
	doclist = get_mapped_doc(
		"Selling Price Simulation",
		source_name,
		{
			"Selling Price Simulation": {
				"doctype": "Quotation",
				"validation": {"status": ["=", "Approved"]},
				"field_map": {
					"name": "selling_price_simulation"
				}
			}
		},
		target_doc,
		set_missing_values
	)
	
	if doclist and len(doclist.items) == 0:
		source_doc = frappe.get_doc("Selling Price Simulation", source_name)
		quotation_item = doclist.append("items", {})
		update_item(None, quotation_item, source_doc)
		
	return doclist
