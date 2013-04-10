# coding: utf-8

import cairo
import pycha.bar
import pycha.pie
import copy
import string
from PIL import Image

class PhilDisplay:

	def __init__(self, label, filename=None, height=None, width=None):
		self.label = label
		self.filename = filename or label + ".png"
		self.datasets = []
		
		self.height = height or 700
		self.width = width or 1000
		self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)

	def prepare_chart(self, chartType, dataset=None, options=None):
		if chartType=='bar':
			self.chartType = pycha.bar.VerticalBarChart
		elif chartType=='pie':
			self.chartType = pycha.pie.PieChart

		self.options = options or {}
		self.chart = self.chartType(self.surface, self.options)
		if dataset:
			self.add_dataset(dataset)

	def _prepare_data(self, amounts, datalabel=None):
		datalabel = (datalabel or self.label)
		if self.chartType == pycha.bar.VerticalBarChart:
			return ((datalabel, [(i, l[1]) for i, l in enumerate(amounts)]),)
		elif self.chartType == pycha.pie.PieChart:
			return [(amount[0], [[0, amount[1]]]) for amount in amounts]

	def add_dataset(self, dataset, datalabel=None):
		self.datasets.append(dataset)
		self.chart.addDataset(self._prepare_data(self.datasets[-1], datalabel))

	def finish(self):
		self.chart.render()
		self.surface.write_to_png(self.filename)

	def show(self):
		im = Image.open(self.filename)
		im.show()

		



