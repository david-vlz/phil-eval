#!/usr/bin/python
# coding: utf-8

class Validator:

	def __init__(self):
		self.value_spaces = {}

	def add_value_space(self, spacename, values):
		self.value_spaces[spacename] = values;
