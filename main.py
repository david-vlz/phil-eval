#!/usr/bin/python
# coding: utf-8

import xlrd

from stats import *
from validator import *

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


