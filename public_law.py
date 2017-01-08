#! /usr/bin/python

# public_law.py

class PublicLaw:
	def __init__(self, law_id, title, date_enacted=None, description=None, amended_titles=None):
		self.law_id = law_id
		self.title = title
		self.date_enacted = date_enacted
		self.description = description
		self.amended_titles = amended_titles

		return
