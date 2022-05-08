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