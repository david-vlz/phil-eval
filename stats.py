#!/usr/bin/python
# coding: utf-8

from xlrd import *

"""
Eine einzelne Tabellenzeile

coln: die Zeilennummer im Excel sheet
id: die interne id der Spalte, wenn vorhanden
name: der Klarname der Spalte, wenn vorhanden
valid_values: eine Liste mit erlaubten Werten
"""
class Column:

	def __init__(self, number, id, name="", validator=None):
		self.number = number
		self.id = id
		self.name = name
		if validator:
			self.validator = validator

	def validate(self, value):
		if self.validator:
			return self.validator.validate(self.name, value)

	def get_allowed_values(self):
		if self.validator:
			return self.validator.get_value_space(self.name)

"""
Ein einzelnes Datum
"""
class Field:

	def __init__(self, value, x_pos, y_pos, column=None, additional_value=None):
		self.value = value
		self.x = x_pos
		self.y = y_pos
		self.column = column
		# ein zusätzlicher Wert, der bei der Validierung nicht einbeezogen wird
		self.additional_value = additional_value

	def validate(self):
		if self.column:
			return self.column.validate(self.value)


class Record:

	def __init__(self, fields=None):
		self.fields = fields or []

	def add_field(self, field):
		self.fields.append(field)

	def iter_fields(self):
		for field in self.fields:
			yield (field.value, field.column)

	def get_field_by_column(self, column):
		for field in self.fields:
			if not(cmp(field.column, column)):
				return field
		return None

	def get_field_by_column_name(self, name):
		for field in self.fields:
			if field.column.name == name:
				return field
		return None

	def get_value(self, column_name):
		for value, column in self.iter_fields():
			if column.name == column_name:
				return value

	def prepare(self):
		return True;


"""
Definiert eine Referenz für die gesamte Tabelle
"""
class Table:

	"""
	Tabelle sollte eine Zeile mit Spalten-Indices und eine Spalte mit 
	Spaltennamen enthalten. (Standardmäßig werden die in der ersten und zweiten 
	Zeile vermutet. (Die kann auch auf None gesetzt werden). 
	Alle Zeilen darunter bis zum Offset werden als einzelne 
	Datensätze behandelt.

	Argumente:
		sheet: Ein xlrd.sheet Objekt, das die eigentliche Tabelle enthält
		x_offset = Anzahl der zu betrachtenden Spalten, entspricht der
			Anzahl der Felder in der ersten Zeile, wenn nicht gesetzt
		y_offset = Anzahl der zu betrachtenden Zeilen, entspricht der
			Anzahl der Felder in der ersten Spalte, wenn nicht gesetzt
		index_row: Nummer der Kopfzeile mit id Werten der einzelnen 
			Spalten
		name_row: Nummer der Kopfzeile mit aussagekräftigen Namen
			der einzelnen Spalten
	"""
	def __init__(self, sheet, record_class=None, validator=None, 
				 index_row=0, name_row=1,
				 x_offset = None, y_offset = None):
		if not(x_offset):
			x_offset = len(sheet.row(index_row))
		if not(y_offset):
			y_offset = len(sheet.col(index_row))

		self.columns = []
		self.records = []
		self.record_class = record_class or Record

		start_row_number = max(index_row, name_row) + 1

		col_name = None
		for x in range(0, x_offset):
			# Neue Spalten anlegen
			col_id = _normalize_value(sheet.cell(index_row, x))
			if (name_row):
				col_name = _normalize_value(sheet.cell(name_row, x))
			col = Column(x, col_id, (col_name or ""), validator)
			self.columns.append(col);

			# Felder anlegen und dem entsprechenden Datensatz übergeben
			for y in range(start_row_number, y_offset):
				if x == 0:
					self.records.append(self.record_class())
				field = Field(sheet.cell(y,x).value, x, y, col)
				self.records[y-start_row_number].add_field(field)

	def get_invalids_by_column(self, col_nr):
		invalids = []
		column = self.get_column_by_number(col_nr)
		for record in self.records:
			field = record.get_field_by_column(column)
			if field.value and not(field.validate()):
				invalids.append(field)
		return invalids

	def get_column_by_number(self, number):
		if self.columns[number].number == number:
			return self.columns[number]
		else:
			for column in self.columns:
				if column.number == number:
					return column

	def get_column_by_name(self, name):
		for column in self.columns:
			if column.name == name:
				return column

	def prepare_all(self):
		for record in self.records:
			record.prepare()

	def get_amounts(self, column_name, record_base=None):
		result = {}
		if not(record_base):
			record_base = self.records
		values = self.get_column_by_name(column_name).get_allowed_values()
		for record in record_base:
			value = record.get_value(column_name)
			if (type(values) == list) and not(value in values):
				value = 'Other'
			result[value] = result.get(value, 0) + 1
		return result

	def get_amounts_as_tuples(self, column_name, record_base=None):
		amounts = self.get_amounts(column_name, record_base)
		tuples = [ (key, amounts[key]) for i, key in enumerate(amounts)]
		return tuple(tuples)



invalids = []
def get_invalids(row_nr):
	for val, y, x in invalids:
		if x == row_nr:
			print repr(val), y, x






"""
Den Inhalt einer Zelle in einen String umwandeln. Notwendig vor allem für
Tabellenköpfe und Wertlisten, die einen Mix aus Zahlen und Strings enthalten.

Argumente:
	cell: Eine einzelne Zelle eines xlrd sheets
Rückgabe:
	der Zelleninhalt als String. Bei Floats wird .0 ggf. weggekürzt
"""
def _normalize_value(cell):
	cell_type = cell.ctype
	cell_value = cell.value
	if cell_type == XL_CELL_TEXT:
		return cell.value
	elif cell_type == XL_CELL_NUMBER:
		if (cell_value % 1) == 0:
			return str(int(cell_value))
		else:
			return str(cell_value)
	else:
		return str(cell_value)
