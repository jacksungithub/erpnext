frappe.listview_settings['Selling Price Simulation'] = {
	add_fields: ["status", "item_code", "suggested_selling_price", "company"],
	get_indicator: function(doc) {
		if (doc.status === "Approved") {
			return [__("Approved"), "green", "status,=,Approved"];
		} else if (doc.status === "Pending Approval") {
			return [__("Pending Approval"), "orange", "status,=,Pending Approval"];
		} else if (doc.status === "Rejected") {
			return [__("Rejected"), "red", "status,=,Rejected"];
		} else {
			return [__("Draft"), "grey", "status,=,Draft"];
		}
	}
};
