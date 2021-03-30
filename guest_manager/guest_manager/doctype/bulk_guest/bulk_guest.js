// Copyright (c) 2021, Victor Maduforo and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bulk Guest', {
	refresh: function(frm) {
		frm.add_custom_button('Add Guest', function(){
			var guest = new frappe.ui.Dialog({
				title: "Add a guest",
				fields: [
					{label: "First name", fieldname: "guest_first_name", fieldtype: "Data"},
					{label: "Last name", fieldname: "guest_last_name", fieldtype: "Data"},
					{label: "Phone number", fieldname: "guest_phone_number", fieldtype: "Data"},
					{label: "Email", fieldname: "email", fieldtype: "Data", options: "Email"}
				],
				primary_action_label: "Add",
				primary_action(values){
					frm.add_child("guests", {
						resident: frm.doc.resident,
						guest_first_name: values.guest_first_name,
						guest_last_name: values.guest_last_name,
						guest_phone_number: values.guest_phone_number,
						email: values.email,
						expected_arrival_time: frm.doc.expected_arrival_time
					})
					frm.refresh_field("guests");
					guest.hide();
				}
			})
			guest.show();
		})
	}
});
