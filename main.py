#!/usr/bin/python
# coding: utf-8

import xlrd

from stats import *
from validate import *
from mappings import mappings
from phil_stats import *


# Excel-Tabellen bereithalten
book = xlrd.open_workbook('data.xls')
main_sheet = book.sheet_by_index(2)
valid_fields_sheet = book.sheet_by_index(1)

# Erlaubte Feldwerte in den Validator einlesen
validator = Validator();
for i in range(0, len(valid_fields_sheet.row(0))):
	field_list = []
	column = valid_fields_sheet.col(i)
	name = column[0].value
	for j in range(1, len(column)):
		field_list.append(column[j].value)
	validator.add_value_space(name, [x for x in field_list if x != ''])

# Aliase an Validator übergeben
for k, v in mappings.items():
	validator.add_spacename_alias(k, v)

t = PhilTable(main_sheet, PhilRecord, validator)
t.prepare_all()
r = t.records[11]


def check(column_nr):
	t = PhilTable(main_sheet, PhilRecord, validator)
	t.prepare_all();
	invs = t.get_invalids_by_column(column_nr)
	for field in invs:
		print (field.y, repr(field.value), field.column.name)


