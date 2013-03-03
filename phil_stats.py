import stats

class PhilTable(stats.Table):

	def bla(self):
		print 'blubb'


class PhilRecord(stats.Record):

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
					field.value = float(elems[0]) + (float(elems[1])/10)

	def extract_additional_value(self, field, value_introduction_string):
		if field.value.find(value_introduction_string) == 0:
			value = field.value
			intro_end_index = len(value_introduction_string)
			field.value = value[:intro_end_index]
			field.additional_value = value[intro_end_index:]