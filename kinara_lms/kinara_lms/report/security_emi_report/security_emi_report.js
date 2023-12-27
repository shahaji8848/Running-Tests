// Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
// For license information, please see license.txt

frappe.query_reports["Security EMI Report"] = {
	"filters": [
		{
			"fieldname" : "name1",
			"label" : "Name",
			"fieldtype" : "Data"	
		},
		{
			"fieldname" : "group",
			"label" : "Group",
			"fieldtype" : "Data"	
		},
		{
			"fieldname" : "brand_name",
			"label" : "Brand",
			"fieldtype" : "Data"	
		}
	],
	// "formatter": function(value, row, column, data, default_formatter) {
	// 	value = default_formatter(value, row, column, data);
	// 	console.log(column.fieldname)
	// 	if (column.fieldname == "group" && data.group == "Vegetable")
	// 	{
	// 	value = "<span style='color:red'>" + value + "</span>";
	// 	}
	// 	else if(column.fieldname == "group")
	// 	{
	// 	value = "<span style='color:green'>" + value + "</span>";
	// 	}
	// 	return value;
	// },
};

	