#!/usr/bin/python
# coding: utf-8

import xlrd

from stats import *
from validate import *
from mappings import mappings

class PhilRecord(Record):

	def prepare(self):
		col_names = [u'Zeit Vorbereitung Intensiv', 
			u'Zeit Nachbereitung Intensiv',
			u'Zeit Lesen Intensiv',
			u'Leistungspunkte Intensiv',
			u'Art Veranstaltung Intensiv',
			u'Zeit Vorbereitung Durchschnittlich', 
			u'Zeit Nachbereitung Durchschnittlich',
			u'Zeit Lesen Durchschnittlich',
			u'Leistungspunkte Durchschnittlich',
			u'Art Veranstaltung Durchschnittlich',
			u'Arbeitszeit']
		for name in col_names:
			field = self.get_field_by_column_name(name)
			self.to_ger_float(field)

		col_names = [u'Art Veranstaltung Intensiv',
			u'Art Veranstaltung Durchschnittlich']
		for name in col_names:
			field = self.get_field_by_column_name(name)
			self.extract_additional_value(field, 'Andere: ')

		col_names = [u'Berufliches Ziel',
			u'Gr\xfcnde Fehlen Obligatorische',
			u'Was hat abgehalten?']
		for name in col_names:
			field = self.get_field_by_column_name(name)
			self.extract_additional_value(field, 'Sonstiges: ')

		field = self.get_field_by_column_name(u'Einkunft Sonstiges:')
		self.extract_additional_value(field, 'Ja, ')


	def to_ger_float(self, field):
		if type(field.value) != float:
			no_str = field.value
			if ',' in no_str:
				elems = no_str.split(',')
				if len(elems) == 2:
					try:
						field.value = float(elems[0]) + (float(elems[1])/10)
					except:
						print 'Error in Conversion: ', field.y, field.column.name

	def extract_additional_value(self, field, value_introduction_string):
		if field.value.find(value_introduction_string) == 0:
			value = field.value
			intro_end_index = len(value_introduction_string)
			field.value = value[:intro_end_index]
			field.additional_value = value[intro_end_index:]



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

t = Table(main_sheet, PhilRecord, validator)
r = t.records[11]


def check(column_nr):
	t = Table(main_sheet, PhilRecord, validator)
	t.prepare_all();
	invs = t.get_invalids_by_column(column_nr)
	for field in invs:
		print (field.y, repr(field.value), field.column.name)