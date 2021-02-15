// Copyright (c) 2021, Victor Maduforo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Resident', {
	// refresh: function(frm) {

	// }
	before_save: function(frm) {
        frm.doc.full_name = frm.doc.first_name + ' ' + frm.doc.last_name;
    }
});
