# Copyright (c) 2023, Visage Holdings and Finance Private Limited) and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
	columns, data = [], [['A','B',"C",'D','E']]
	columns = [
		_("Name")+ "::200",
		_("Group")+ "::200",
		_("Quantity")+ "::200",
		_("Rate")+ "::200",
		_("Brand")+ "::200"
	]
	condition = []
	if filters.name1:
		condition.append(f"ci.name1 LIKE '%%{filters.name1}%%'")
	if filters.group:
		condition.append("ci.group LIKE %(group)s")
		filters.group = f"%{filters.group}%"
	if filters.brand_name:
		condition.append(f"brand.brand_name LIKE '%%{filters.brand_name}%%'")
	if len(condition) > 1:
		condition_clause = f"WHERE " + "AND ".join(condition)
	elif len(condition) == 1:
		condition_clause = "WHERE " + condition[0]
	else:
		condition_clause = ""
	# mydata = frappe.db.sql(f"""
	# 						SELECT ci.`name1`, ci.`group`, ci.`quantity`, ci.`rate`, brand.`brand_name`
	# 						FROM `tabCustom Item` as ci
	# 						JOIN `tabCustom Brand` as brand
	# 						ON brand.parent = ci.name
	# 						{condition_clause}""", filters)
	return columns,data

