# Copyright (c) 2022, Javier Rangel and contributors
# For license information, please see license.txt

from wsgiref import validate
import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
	
	# validar membresia activa y disponibilidad del articulo
	def before_submit(self):
		if self.type == 'Emitido':
			self.validate_issue()
			self.validate_maximum_limit()
			article = frappe.get_doc('Articulo', self.article)
			article.status = 'Issue'
			article.save()

		elif self.type == 'Disponible':
			self.validate_return()
			article = frappe.get_doc('Articulo', self.article)
			article.status = 'Available'
			article.save()

	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc('Articulo', self.article)
		if article.status == 'Emitido':
			frappe.throw('El articulo ha sido solicitado por otro usuario')

	def validate_return(self):
		article = frappe.get_doc('Articulo', self.article)
		if article.status == 'Disponible':
			frappe.throw('El articulo no se puede devolver sin ser solicita')

	def validate_maximum_limit(self):
		max_articles = frappe.db,get_single_value('Library Settings', 'max_article')
		count = frappe.db.count(
			'Library Transaction',
			{
				'library_member': self.library_member,
				'type': 'Emitido',
				'docstatus': 1,
			},
		)
		if count >= max_articles:
			frappe-throw('Has alanzado el limite maximo de articulos!')

	def validate_membership(self):
		validate_membership = frappe.db.exists(
			'Library Membership',
			{
				'library_member': self.library_member,
				'docstatus': 1,
				'from_date': ('>', self.date),
				'to_date': ('>', self.date),
			},
		)
		if not validate_membership:
			frappe.throw('El miembro no tiene una membresia valida!')