# Copyright (c) 2022, Javier Rangel and contributors
# For license information, please see license.txt

from wsgiref import validate
import frappe
from frappe.model.document import Document

class LibraryTransaction(Document):
	
	# metodos de validacion
	def before_submit(self):
		"""funcion que hace referencia a Issue de Library Trasaction"""

		if self.type == 'Issue': # esto es de Library Transaction
			self.validate_issue()
			self.validate_maximum_limit()
			article = frappe.get_doc('Articulo', self.article)
			article.status = 'Emitido' # debe ser igual a como se declaro en el doctype de referencia
			article.save()

		elif self.type == 'Return': # esto es de Library Transaction
			self.validate_return()
			article = frappe.get_doc('Articulo', self.article)
			article.status = 'disponible' # debe ser igual a como se declaro en el doctype de referencia
			article.save()

# funcion validate_issue OK
# la funcion hace referencia al doctype Articulo
	def validate_issue(self):

		self.validate_membership()
		article = frappe.get_doc('Articulo', self.article)
		if article.status == 'Emitido':
			frappe.throw('El articulo ha sido solicitado por otro usuario')

# funciona validate_return OK
	def validate_return(self):

		# hace referencia al doctype Articulo
		article = frappe.get_doc('Articulo', self.article)
		if article.status == 'disponible':
			frappe.throw('El articulo no se puede devolver sin ser solicitado!')
# funcion ok
	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value('Library Settings', 'max_articles')
		count = frappe.db.count(
			'Library Transaction',
			{
				'library_member': self.library_member,
				'type': 'Issue',
				'docstatus': 1,
			},
		)
		if count >= max_articles:
			frappe.throw('Has alanzado el limite maximo de articulos!')

# funciona OK
	def validate_membership(self):
		valid_membership = frappe.db.exists(
			'Library Membership',
			{
				'library_member': self.library_member,
				'docstatus': 1,
				'from_date': ('<', self.date),
				'to_date': ('>', self.date),
			},
		)
		if not valid_membership:
			frappe.throw('El miembro no tiene una membresia valida!')