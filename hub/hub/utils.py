# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
import os
import requests
import base64
from frappe.utils import cint

def autoname_increment_by_field(doctype, field_name, name):
	count = frappe.db.count(doctype, {field_name: name})
	if cint(count):
		return '{0}-{1}'.format(name, count)
	else:
		return name

def save_remote_file_locally(file_url, doctype, name):
	'''
	Takes an absolute URL like https://example.com/test.jpg,
	downloads it, saves it locally, and creates a new File record
	'''
	if not file_url.startswith('http'):
		return

	file_name = os.path.basename(file_url)
	# url may contain query string
	file_name = file_name.rsplit('?')[0]

	response = requests.get(file_url)

	f = None
	if response.ok:
		f = frappe.get_doc({
			'doctype': 'File',
			'file_name': file_name,
			'attached_to_doctype': doctype,
			'attached_to_name': name,
			'content': response.content
		})

		f.save()

	return f

def check_user_and_item_belong_to_same_seller(hub_user,hub_item_name):
	'''
	Check if item and user belong to same seller.
	'''
	item_hub_seller_name = frappe.db.get_value('Hub Item', hub_item_name, fieldname=['hub_seller'])
	if item_hub_seller_name != frappe.db.get_value('Hub User', hub_user, fieldname=['hub_seller']):
		frappe.throw(_("You can only feature your own published items"))
	return
