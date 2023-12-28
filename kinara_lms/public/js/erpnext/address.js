frappe.ui.form.on("Address", {
    geo_type_id: function(frm){
        setState(frm);
    },
});
function setState(frm){
    frappe.call({
        method: 'frappe.client.get_value',
        args: {
            'doctype': 'Geo',
            'filters': {'name': frm.doc.geo_type_id},
            'fieldname': [
                'state',
            ]
        },
        callback: function(response) {
            if (response.message.hasOwnProperty('state')) {
                frm.set_value("state", response.message.state);
            }
            else{
                frm.set_value("state", null);
            }
        }
    });
}