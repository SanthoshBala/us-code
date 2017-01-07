#! /usr/bin/python

# chamber.py

class Chamber:
	def __init__(self, ordinality, chamber, democrats, republicans, 
					democratic_leader, republican_leader, others=0, 
					first_year=None, last_year=None):
		self.ordinality = ordinality
		self.chamber = chamber
		self.democrats = democrats
		self.republicans = republicans
		self.democratic_leader = democratic_leader
		self.republican_leader = republican_leader
		self.others = others
		self.first_year = first_year
		self.last_year = last_year

		return
