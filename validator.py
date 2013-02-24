#!/usr/bin/python
# coding: utf-8


class Validator:

	def __init__(self, value_spaces={}, spacename_aliases={}):
		self.value_spaces = value_spaces
		self.spacename_aliases = spacename_aliases

	def add_value_space(self, spacename, values):
		self.value_spaces[spacename] = values

	def get_value_space(self, spacename):
		spacename = self.get_proper_spacename(spacename)
		return self.value_spaces.get(spacename)

	def add_spacename_alias(self, alias, spacename):
		if self.value_spaces.has_key(spacename):
			self.spacename_aliases[alias] = spacename
		else:
			raise NotASpaceNameError(spacename)

	def get_proper_spacename(self, possible_alias):
		if self.value_spaces.has_key(possible_alias):
			return possible_alias
		else:
			return self.spacename_aliases.get(possible_alias)

	def validate(self, spacename, value):
		proper_spacename = self.get_proper_spacename(spacename)
		try:
			return (value in self.get_value_space(proper_spacename))
		except TypeError:
			raise NotASpaceNameError(spacename)
	


class NotASpaceNameError(Exception):

	def __init__(self, spacename):
		self.value = spacename

	def __str__(self):
		return repr(self.value) + ' does not name a value space'

