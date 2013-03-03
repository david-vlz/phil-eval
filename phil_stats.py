import stats

BA_STUDIES = [
	u'Bachelor (Wissenschaftlich)',
	u'Bachelor Lehramt Philosophie / Praktische Philosophie GyGe',
	u'Bachelor Lehramt Praktische Philosophie HRGe'

]

MA_STUDIES = [
	u'Master (Wissenschaftlich)'
]

OLD_STUDIES = [
	u'Magister(Wissenschaftlich)',
	u'Lehramt f\xfcr Sek I/II (LPO 1997)',
	u'Lehramt GyGe (LPO 2003)',
	u'Lehramt HRGe',
	u'Sonderp\xe4dagogik',
	u'Diplomstudiengang P\xe4dagogik'
]

TEACHING_SUBJECTS = [
	u'Lehramt f\xfcr Sek I/II (LPO 1997)',
	u'Lehramt GyGe (LPO 2003)',
	u'Lehramt HRGe',
	u'Bachelor Lehramt Philosophie / Praktische Philosophie GyGe',
	u'Bachelor Lehramt Praktische Philosophie HRGe',
	u'Sonderp\xe4dagogik',
	u'Diplomstudiengang P\xe4dagogik'
]

NON_TEACHING_SUBJECTS = [
	u'Magister(Wissenschaftlich)',
	u'Bachelor (Wissenschaftlich)',
	u'Master (Wissenschaftlich)'
]


class PhilTable(stats.Table):

	def bama_students(self):
		result = []
		for record in self.records:
			if record.studies_bama:
				result.append(record)
		return result

'''
Felder:
	.studies_bama
	.studies_older
	.studies_teach
	.studies_nonteach
'''

class PhilRecord(stats.Record):

	def prepare(self):
		'''
		Feldinhalte vorbereiten, bzw. vereinheitlichen
		'''
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

		'''
		Abstrakte Eigenschaften ermitteln
		'''
		self.subject = self.get_value('Studiengang')
		if (self.subject in BA_STUDIES or self.subject in MA_STUDIES):
			self.studies_bama = True
			self.studies_older = False
		elif (self.subject in OLD_STUDIES):
			self.studies_bama = False
			self.studies_older = True
		else:
			self.studies_bama = None
			self.studies_older = None
		if (self.subject in TEACHING_SUBJECTS):
			self.studies_teach = True
			self.studies_nonteach = False
		elif (self.subject in NON_TEACHING_SUBJECTS):
			self.studies_teach = False
			self.studies_nonteach = True
		else:
			self.studies_teach = None
			self.studies_nonteach = None



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