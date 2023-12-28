// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.ui.form.on("Loan ACH", {
    thirty_year_end: function(frm) {
        if (frm.doc.thirty_year_end == 1) {
            if (frm.doc.ach_start_date != undefined && frm.doc.ach_start_date != null) {
                var startDate = frappe.datetime.str_to_obj(frm.doc.ach_start_date);
                var thirtyYearsLater = new Date(startDate.getFullYear() + 30, startDate.getMonth(), startDate.getDate());
                frm.set_value('ach_end_date', thirtyYearsLater);
            } else {
                frm.set_value('thirty_year_end', 0);
                frappe.msgprint("Please Select ACH Start Date First");
            }
        } else {
            frm.set_value('ach_end_date', null);
        }
    },
    ach_start_date: function(frm) {
        if (frm.doc.ach_start_date == undefined && frm.doc.ach_start_date == null) {
            if (frm.doc.ach_end_date != undefined && frm.doc.ach_end_date != null) {
                frm.set_value('ach_end_date', null);
                frm.set_value('thirty_year_end', 0);

            }
        }
    }
});
