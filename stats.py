#!/usr/bin/python
# coding: utf-8

from xlrd import *

"""
Eine einzelne Tabellenzeile

coln: die Zeilennummer im Excel Stylesheet
id: die interne id der Spalte, wenn vorhanden
name: der Klarname der Spalte, wenn vorhanden
valid_values: eine Liste mit erlaubten Werten
"""
class Column:

	def __init__(self, number, id, name="", valid_content=None):
		self.number = number
		self.id = id
		self.name = name
		self.valid_content = valid_content


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
	def __init__(self, sheet, validator=None, 
				 index_row=0, name_row=1,
				 x_offset = None, y_offset = None):
		if not(x_offset):
			x_offset = len(sheet.row(index_row))
		if not(y_offset):
			y_offset = len(sheet.col(index_row))

		self.columns = []
		col_name = None
		for i in range(0, x_offset):
			col_id = normalize_value(sheet.cell(index_row, i))
			if (name_row):
				col_name = normalize_value(sheet.cell(name_row, i))
			col = Column(i, col_id, (col_name or ""))
			self.columns.append(col);

		# self.indices = map(normalize_value, sheet.row(header_idx_row))
		# self.names = map(normalize_value, sheet.row(header_name_row))







"""
Den Inhalt einer Zelle in einen String umwandeln. Notwendig vor allem für
Tabellenköpfe und Wertlisten, die einen Mix aus Zahlen und Strings enthalten.

Argumente:
	cell: Eine einzelne Zelle eines xlrd sheets
Rückgabe:
	der Zelleninhalt als String. Bei Floats wird .0 ggf. weggekürzt
"""
def normalize_value(cell):
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
