# -*- coding: utf-8 -*-
# Copyright (c) 2021, Victor Maduforo and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class Bookings(Document):
	def validate(self):
		if self.start_time < frappe.utils.nowdate():
			frappe.throw('Start time should not be earlier than current time')
		if self.end_time:
			if self.start_time > self.end_time:
				frappe.throw('Start time should not be later than end time')
			if self.start_time == self.end_time:
				frappe.throw('Start time should not be same as end time')
