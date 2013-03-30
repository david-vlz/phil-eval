# coding: utf-8

import cairo
import pycha.bar
from PIL import Image

# Maße der Cairo-Oberfläche
width, height = (1000, 700)

# Optionen für die PyCha charts
# options = {
#     'legend': {'hide': True},
#     'background': {'color': '#f0f0f0'},
# }

options = {
    'legend': {'hide': False},
    'background': {'color': '#2dbcb0'}
}

def _to_bar_chart(dataset):
	surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
	chart = pycha.bar.VerticalBarChart(surface, options)
	chart.addDataset(dataset)
	chart.render()
	return surface

def save_as_bar_chart(dataset, filename):
	surface = _to_bar_chart(dataset)
	surface.write_to_png(filename)

def show_as_bar_chart(dataset, filename):
	save_as_bar_chart(dataset, filename)
	im = Image.open(filename)
	im.show()


