#!/usr/bin/python
# coding: utf-8

class Validator:

	def __init__(self):
		self.value_spaces = {}

	def add_value_space(self, spacename, values):
		self.value_spaces[spacename] = values

	def get_value_space(self, spacename):
		return self.value_spaces.get(spacename, None)

	def validate(self, spacename, value):
		return (value in self.get_value_space(spacename))
	
	# def validate(self, )

