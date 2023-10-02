frappe.ui.form.on("Loan Partner", {
	refresh(frm) {
        frm.events.toggle_processing_fee_billing(frm);
    },

    toggle_processing_fee_billing(frm) {
        if(!frm.doc.shareables || !frm.doc.shareables.some(s => s.shareable_type === "Processing fee")) {
			frm.toggle_display("processing_fee_billing", 0);
		} else {
            frm.toggle_display("processing_fee_billing", 1);
        }
    }
});

frappe.ui.form.on('Loan Partner Shareable', {
	shareable_type(frm) {
        frm.events.toggle_processing_fee_billing(frm);
	}
});
