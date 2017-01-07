#! /usr/bin/python

# potus.py

class POTUS:
	def __init__(self, ordinality, first_name, last_name, party, 
					first_year=None, last_year=None, middle_name=None, 
					nickname=None):
		self.ordinality = ordinality
		self.first_name = first_name
		self.last_name = last_name
		self.party = party
		self.first_year = first_year
		self.last_year = last_year
		self.middle_name = middle_name
		self.nickname = nickname

		return
