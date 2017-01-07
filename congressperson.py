#! /usr/bin/python

# congressperson.py

class Congressperson:
	def __init__(self, first_name, last_name, chamber, party, 
					state, first_year=None, last_year=None, 
					middle_name=None, nickname=None):
		self.first_name = first_name
		self.last_name = last_name
		self.chamber = chamber
		self.party = party
		self.state = state
		self.first_year = first_year
		self.last_year = last_year
		self.middle_name = middle_name
		self.nickname = nickname

		return
