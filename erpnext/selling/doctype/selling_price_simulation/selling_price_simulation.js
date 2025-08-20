
frappe.ui.form.on('Selling Price Simulation', {
	refresh: function(frm) {
		if (frm.doc.status === "Draft") {
			frm.add_custom_button(__('Submit for Approval'), function() {
				frm.call('submit_for_approval').then(() => {
					frm.refresh();
				});
			});
		}
		
		if (frm.doc.status === "Pending Approval" && frappe.user.has_role("Sales Manager")) {
			frm.add_custom_button(__('Approve'), function() {
				frm.call('approve_simulation').then(() => {
					frm.refresh();
				});
			}, __('Actions'));
			
			frm.add_custom_button(__('Reject'), function() {
				frm.call('reject_simulation').then(() => {
					frm.refresh();
				});
			}, __('Actions'));
		}
		
		if (frm.doc.status === "Approved") {
			frm.add_custom_button(__('Make Quotation'), function() {
				frappe.model.open_mapped_doc({
					method: "erpnext.selling.doctype.selling_price_simulation.selling_price_simulation.make_quotation",
					frm: frm
				});
			}, __('Create'));
		}
		
		if (frm.doc.status) {
			let indicator_color = {
				"Draft": "grey",
				"Pending Approval": "orange", 
				"Approved": "green",
				"Rejected": "red"
			};
			frm.dashboard.set_headline_alert(
				`<div class="indicator ${indicator_color[frm.doc.status]}">
					${__('Status')}: ${__(frm.doc.status)}
				</div>`
			);
		}
	},
	
	company: function(frm) {
		if (frm.doc.company) {
			frappe.db.get_value('Company', frm.doc.company, 'default_currency')
				.then(r => {
					if (r.message && r.message.default_currency) {
						frm.set_value('currency', r.message.default_currency);
					}
				});
		}
	},
	
	currency: function(frm) {
		if (frm.doc.currency && frm.doc.company) {
			frappe.db.get_value('Company', frm.doc.company, 'default_currency')
				.then(r => {
					if (r.message && r.message.default_currency) {
						let company_currency = r.message.default_currency;
						if (frm.doc.currency !== company_currency) {
							frappe.call({
								method: "erpnext.setup.utils.get_exchange_rate",
								args: {
									from_currency: frm.doc.currency,
									to_currency: company_currency,
									transaction_date: frappe.datetime.get_today()
								},
								callback: function(r) {
									if (r.message) {
										frm.set_value('conversion_rate', r.message);
									}
								}
							});
						} else {
							frm.set_value('conversion_rate', 1.0);
						}
					}
				});
		}
	}
});

frappe.ui.form.on('Selling Price Simulation Supplier Offer', {
	price_usd: function(frm, cdt, cdn) {
		frm.trigger('calculate_costs');
	},
	
	supplier_offers_remove: function(frm) {
		frm.trigger('calculate_costs');
	}
});

frappe.ui.form.on('Selling Price Simulation', {
	calculate_costs: function(frm) {
		frm.save();
	}
});
