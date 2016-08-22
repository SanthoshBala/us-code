#!/usr/bin/python

# olrc-differ.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides the ability to see diffs between any two USC title XML files.

from difflib import Differ
from pprint import pprint

class OlrcDiffer:

	CODE_FORMAT_XHTML = "xhtml"

	def __init__(self, preFileName, postFileName, format=CODE_FORMAT_XHTML):
		self.preFile = open(preFileName, 'r').read().splitlines(True)
		self.postFile = open(postFileName, 'r').read().splitlines(True)
		self.diff = Differ()

		return

	def printDiff(self):
		diffLines = list(self.diff.compare(self.preFile, self.postFile))
		pprint(diffLines)

	def writeDiff(self):
		diffLines = list(self.diff.compare(self.preFile, self.postFile))
		outFile = open("diffFile.txt", 'w')
		for line in diffLines:
			outFile.write(line)

		outFile.close()
