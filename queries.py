#!/usr/bin/python
# coding: utf-8

import xlrd
import copy

import validate
import phil_stats
import display
from mappings import mappings

def dict_merge(a, b):
    '''recursively merges dict's. not just simple a['key'] = b['key'], if
    both a and bhave a key who's value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.'''
    if not isinstance(b, dict):
        return b
    result = copy.deepcopy(a)
    for k, v in b.iteritems():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = copy.deepcopy(v)
    return result

# Excel-Tabellen bereithalten
book = xlrd.open_workbook('data.xls')
main_sheet = book.sheet_by_index(2)
valid_fields_sheet = book.sheet_by_index(1)

# Erlaubte Feldwerte in den Validator einlesen
validator = validate.Validator();
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

# Haupttabelle initialisieren und vorbereiten
t = phil_stats.PhilTable(main_sheet, phil_stats.PhilRecord, validator)
t.prepare_all()

options = {
	'legend': {'hide': True },
	'colorScheme': {
		'name': 'gradient',
		'args': {
			'initialColor': 'blue',
		},
	},
	'background': {
		'baseColor': '#f5f5f5'
	},
	'padding': {
		'left': 50,
		'right': 60,
		'top': 50,
		'bottom': 50,
	},
	'yvals': {
		'show': True
	}
}

bar_options =  {
	'axis': {
		'x': {
			'label': None,
			'rotate': 85,
			'interval': 0
		},
	    'y': {
			'ticks': [dict(v=x*10, label=x*10) for x in range(0, 30)],
			'rotate': 0,
			'label': 'Nennungen absolut'
		}
	}
}


def prepare_amounts_query(label, data=None, opts=None):
	d = display.PhilDisplay(label)
	local_options = dict_merge(options, bar_options)
	if data:
		local_options['axis']['x']['ticks'] = [dict(v=i, label=l[0]) for i, l in enumerate(data)]
	final_options = None
	if opts:
		final_options = dict_merge(local_options, opts)
	d.prepare_chart('bar', data, (final_options or local_options))
	return d

def amountsQuery(label, data, opts=None):
	d = prepare_amounts_query(label, data, opts)
	d.finish()
	d.show()

def averagesQuery(averages):
	if averages:
		print 'Durchschnitt: ', averages['average']
		print 'gesamt:', averages['valid'] + averages['invalid'], u'(ungültig:', averages['invalid'], "\b)"


# ANGABEN ZUR PERSON

# Studiengänge abfragen
# tups = t.get_amounts_as_tuples(u'Studiengang')
# amountsQuery(u'Studienngange', tups)

# Fachsemester abfragen
# Durchschnitt insgesamt
# averagesQuery(t.average(u'Fachsemester'))

# Durchschnitte nach Studiengängen
# tups = t.get_amounts_as_tuples(u'Studiengang')
# for tup in enumerate(tups):
# 	subt = t.subtable(u'Studiengang', tup[1][0])
# 	print '---', tup[1][0], '---'
# 	if subt:
# 		avs = subt.average(u'Fachsemester')
# 		averagesQuery(avs)
# 	else:
# 		print 'N/A'
# 	print ''



# WORKLOAD

workload_options =  {
	'legend': {
		'hide': False,
		'position': {
			'right': 25
		}
	},
	'colorScheme': {
		'name': 'gradient'
	},
	'axis': {
		'x': {
			'label': None,
			'rotate': 0,
			'interval': 0,
			'ticks' : [{'v': 0, 'label': 'Zeit Vorbereitung'},
					   {'v': 1, 'label': 'Zeit Nachbereitung'},
					   {'v': 2, 'label': 'Zeit Lesen'} ]
		},
	    'y': {
			'ticks': [dict(v=x, label=x) for x in range(0, 4)],
			'rotate': 0,
			'label': 'Durchscnitt der aufgewendeten Stunden'
		}
	}
}

sem_intensive_cols = [u'Zeit Vorbereitung Intensiv', u'Zeit Nachbereitung Intensiv', u'Zeit Lesen Intensiv']
sem_average_cols = [u'Zeit Vorbereitung Durchschnittlich', u'Zeit Nachbereitung Durchschnittlich', u'Zeit Lesen Durchschnittlich']

def general_workload_averages_query(intensives_table, averages_table):
	d = prepare_amounts_query('Arbeitszeiten', None, workload_options)

	tups_intensive = []
	for col in sem_intensive_cols:
		tups_intensive.append((col, intensives_table.average(col)['average']))
	tups_intensive = tuple(tups_intensive)
	d.add_dataset(tups_intensive, 'Intensiv')

	tups_average = []
	for col in sem_average_cols:
		tups_average.append((col, averages_table.average(col)['average']))
	tups_average = tuple(tups_average)
	d.add_dataset(tups_average, 'Durchschnittlich')
	d.finish()
	return d

def specific_workload_averages_query(cols, *tables):
	d = prepare_amounts_query('Arbeitszeiten', None, workload_options)

	for table in tables:
		tups = []
		for col in cols:
			tups.append((col, table.average(col)['average']))
		tups = tuple(tups)
		d.add_dataset(tups, table.label)

	d.finish()
	return d

# Einfache Arbeitszeiten gegeneinandergehalten
# d = general_workload_averages_query(t, t)
# d.show()

# Arbeitszeitendurchschnitte nach angestrebten CP Filtern
# u = t.subtable(u'Leistungspunkte Intensiv', 4)
# v = t.subtable(u'Leistungspunkte Durchschnittlich', 4)
# d = general_workload_averages_query(u, v)
# d.show()


# Arbeitszeitendurchschnitte nach CP in einer Grafik

# für intensive Seminare
# t4cp = t.subtable(u'Leistungspunkte Intensiv', 4)
# t4cp.label = "4 CP"
# t3cp = t.subtable(u'Leistungspunkte Intensiv', 3)
# t3cp.label = "3 CP"
# t2cp = t.subtable(u'Leistungspunkte Intensiv', 2)
# t2cp.label = "2 CP"
# t1cp = t.subtable(u'Leistungspunkte Intensiv', 1)
# t1cp.label = "1 CP"
# d = specific_workload_averages_query(sem_intensive_cols, t4cp, t3cp, t2cp, t1cp)
# d.show()

#für Seminare mit durchsniitlicher Arbeitszeit
# t4cp = t.subtable(u'Leistungspunkte Durchschnittlich', 4)
# t4cp.label = "4 CP"
# t3cp = t.subtable(u'Leistungspunkte Durchschnittlich', 3)
# t3cp.label = "3 CP"
# t2cp = t.subtable(u'Leistungspunkte Durchschnittlich', 2)
# t2cp.label = "2 CP"
# t1cp = t.subtable(u'Leistungspunkte Durchschnittlich', 1)
# t1cp.label = "1 CP"
# d = specific_workload_averages_query(sem_average_cols, t4cp, t3cp, t2cp, t1cp)
# d.show()


# Arbeitszeitendurchschnitte nach Art des Seminars in einer Grafik

# für intensive Seminare
# tHauptseminar = t.subtable(u'Art Veranstaltung Intensiv', u'Hauptseminar')
# tHauptseminar.label = u'Hauptseminar'
# tProseminar = t.subtable(u'Art Veranstaltung Intensiv', u'Proseminar')
# tProseminar.label = u'Proseminar'
# tVorlesung = t.subtable(u'Art Veranstaltung Intensiv', u'Vorlesung')
# tVorlesung.label = u'Vorlesung'
# d = specific_workload_averages_query(sem_intensive_cols, tHauptseminar, tProseminar, tVorlesung)
# d.show()

# für durchschnittliche Seminare
# tHauptseminar = t.subtable(u'Art Veranstaltung Durchschnittlich', u'Hauptseminar')
# tHauptseminar.label = u'Hauptseminar'
# tProseminar = t.subtable(u'Art Veranstaltung Durchschnittlich', u'Proseminar')
# tProseminar.label = u'Proseminar'
# tVorlesung = t.subtable(u'Art Veranstaltung Durchschnittlich', u'Vorlesung')
# tVorlesung.label = u'Vorlesung'
# d = specific_workload_averages_query(sem_average_cols, tHauptseminar, tProseminar, tVorlesung)
# d.show()




