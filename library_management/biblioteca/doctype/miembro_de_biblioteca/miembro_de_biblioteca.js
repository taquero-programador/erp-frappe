// Copyright (c) 2022, Javier Rangel and contributors
// For license information, please see license.txt

frappe.ui.form.on('Miembro de biblioteca', {
	refresh: function(frm) {
		frm.add_custom_button('Create Membership', () => {
			frappe.new_doc('Library Membership', {
				library_member: frm.doc.name
			})
		})
		frm.add_custom_button('Create Transaction', () => {
			frappe.new_doc('Library Transaction', {
				library_member: frm.doc.name
			})
		})
	}
});
