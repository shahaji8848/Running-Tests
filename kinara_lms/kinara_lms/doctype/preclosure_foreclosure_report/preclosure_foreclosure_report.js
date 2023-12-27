// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.ui.form.on("Preclosure-Foreclosure Report", {
	refresh(frm) {
        let currentDate = new Date();
        console.log(currentDate)
        let year = currentDate.getFullYear();
        let month = currentDate.getMonth() + 1;
        let day = currentDate.getDate();
        let formattedDate = `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day}`;
        frm.set_value("working_date",formattedDate)

        year = currentDate.getFullYear();
        month = String(currentDate.getMonth() + 1).padStart(2, '0'); // Months are zero-based
        day = String(currentDate.getDate()).padStart(2, '0');
        hours = String(currentDate.getHours()).padStart(2, '0');
        minutes = String(currentDate.getMinutes()).padStart(2, '0');
        seconds = String(currentDate.getSeconds()).padStart(2, '0');

        formattedDateTime = `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
        
        frm.set_value("printed_date",formattedDateTime)    
	},
});
