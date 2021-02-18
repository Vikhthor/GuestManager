# -*- coding: utf-8 -*-
# Copyright (c) 2021, Victor Maduforo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from datetime import datetime
import frappe
from frappe.model.document import Document

class Guests(Document):
	def before_save(self):
		self.full_name = f'{self.guest_first_name} {self.guest_last_name or ""}'
		# self.address = frappe.db.get_single_value('Resident','address')
		if self.expected_arrival_time < frappe.utils.nowdate():
			frappe.throw('Arrival time should not be later than current time')
		if self.expected_departure_time:
			if self.expected_arrival_time > self.expected_departure_time:
				frappe.throw('Arrival time should not be later than departure time')
			if self.expected_arrival_time == self.expected_departure_time:
				frappe.throw('Arrival time should not be same as departure time')
	def on_submit(self):
		visit = frappe.new_doc('Visits')
		# visit.resident = frappe.db.get_single_value('Resident','full_name')
		visit.resident = self.resident
		# visit.address = frappe.db.get_single_value('Resident','address')
		visit.address = self.address
		visit.guest = self.full_name
		visit.expected_arrival = self.expected_arrival_time
		visit.expected_departure = self.expected_departure_time
		visit.insert()
	# pass
