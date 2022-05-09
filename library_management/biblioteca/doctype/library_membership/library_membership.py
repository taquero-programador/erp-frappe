# Copyright (c) 2022, Javier Rangel and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class LibraryMembership(Document):
	
	# validar que user no tenga una membresia activa
	def before_submit(self):
		exists = frappe.db.exists(
			'Library Membership',
			{
				'library_member': self.library_member,
				'docstatus': 1,
				'to_date': ('>', self.from_date),
			},
		)
		if exists:
			frappe.throw('Ya tiene una membresia activa!')

		loan_period = frappe.db.get_single_value('Library Settings', 'loan_period')
		self.to_date = frappe.utils.add_days(self.from_date, loan_period or 30)