# coding: utf-8

import cairo
import pycha.bar
from PIL import Image

# Maße der Cairo-Oberfläche
width, height = (1000, 700)

bar_options = {
    'legend': {'hide': True },
    'background': {'color': '#2dbcb0'},
    'padding': {
		'left': 50,
		'right': 50,
		'bottom': 0,
	},
	'colorScheme': {
		'name': 'gradient',
		'args': {
			'initialColor': 'blue',
		},
	},
	'background': {
		# 'chartColor': '#ffeeff',
		'baseColor': '#ffffff'
		# 'lineColor': '#444444'
	},
	'padding': {
		'left': 0,
		'bottom': 0,
	},
}

def _to_bar_chart(amounts, label):
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	options['axis'] = {
		'x': {
			'ticks': [dict(v=i, label=l[0]) for i, l in enumerate(amounts)],
			'label': 'Optionen',
			'rotate': 45
		},
	    'y': {
			'ticks': [dict(v=x*10, label=x*10) for x in range(0, 30)],
			'rotate': 0,
			'label': 'Nennungen absolut'
		}
	}
	options['title'] = label
	chart = pycha.bar.VerticalBarChart(surface, bar_options)
	chart.addDataset(_to_dataset(amounts, label))
	chart.render()
	return surface

def _to_dataset(amounts, label):
	return ( (label, [(i, l[1]) for i, l in enumerate(amounts)]), )

def save_as_bar_chart(amounts, filename):
	surface = _to_bar_chart(amounts, filename)
	surface.write_to_png(filename + '.png')

def show_as_bar_chart(amounts, filename):
	save_as_bar_chart(amounts, filename)
	im = Image.open(filename + '.png')
	im.show()


