#!/usr/bin/python

# olrc-differ.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides the ability to see diffs between any two USC title XML files.

from difflib import Differ
from pprint import pprint
from lxml.html.diff import html_annotate, htmldiff

def version_markup(text, annotation):
	return "<span class=\"%s\">%s</span>" % (annotation, text)

class OlrcDiffer:

	CODE_FORMAT_XHTML = "xhtml"
	METHOD_DIFFER = "differ"
	METHOD_HTML_DIFF = "html_diff"
	METHOD_HTML_ANNOTATE = "html_annotate"
	DIFF_METHOD = METHOD_HTML_DIFF

	def __init__(self, preFileName, postFileName, format=CODE_FORMAT_XHTML):
		if self.DIFF_METHOD == self.METHOD_DIFFER:
			self.preFile = open(preFileName, 'r').read().splitlines(True)
			self.postFile = open(postFileName, 'r').read().splitlines(True)
			self.diff = Differ()
		else:
			self.preFile = open(preFileName, 'r').read()
			self.postFile = open(postFileName, 'r').read()
			# self.preFile = """<p class="statutory-body">In determining the meaning of any Act of Congress, unless the context indicates otherwise&#8212;</p>
							
			# 				<p class="statutory-body-2em">words importing the singular include and apply to several persons, parties, or things;</p>

			# 				<p class="statutory-body-2em">words importing the plural include the singular;</p>

			# 				<p class="statutory-body-2em">words importing the masculine gender include the feminine as well;</p>

			# 				<p class="statutory-body-2em">words used in the present tense include the future as well as the present;</p>"""
			# self.postFile = """<p class="statutory-body">In determining the meaning of any Act of Congress, unless the context indicates otherwise&#8212;</p>

			# 				<p class="statutory-body-1em">words importing the singular include and apply to several persons, parties, or things;</p>

			# 				<p class="statutory-body-1em">words importing the plural include the singular;</p>

			# 				<p class="statutory-body-1em">words importing the masculine gender include the feminine as well;</p>

			# 				<p class="statutory-body-1em">words used in the present tense include the future as well as the present;</p>"""




		return



	def printDiff(self):
		if self.DIFF_METHOD == self.METHOD_DIFFER:
			diffLines = list(self.diff.compare(self.preFile, self.postFile))
			pprint(diffLines)
		elif self.DIFF_METHOD == self.METHOD_LXML:
			print(html_annotate([(self.preFile, 'preYear'),
									(self.postFile, 'postYear')],
									markup=version_markup))

	

	def write(self, outFileName):
		if self.DIFF_METHOD == self.METHOD_DIFFER:
			diffLines = list(self.diff.compare(self.preFile, self.postFile))
			outFile = open("diffFile.txt", 'w')
			for line in diffLines:
				outFile.write(line)

			outFile.close()

		elif self.DIFF_METHOD == self.METHOD_HTML_DIFF:
			outFile = open(outFileName, 'w')
			# outFile.write(html_annotate([(self.preFile, 'preYear'),
			# 						(self.postFile, 'postYear')],
			# 						markup=version_markup).encode('utf-8'))
			outFile.write(htmldiff(self.preFile, self.postFile).encode('utf-8'))
			outFile.close()
		elif self.DIFF_METHOD == self.METHOD_HTML_ANNOTATE:
			outFile = open(outFileName, 'w')
			outFile.write(html_annotate([(self.preFile, 'preYear'),
									(self.postFile, 'postYear')],
									markup=version_markup).encode('utf-8'))
			# outFile.write(htmldiff(self.preFile, self.postFile).encode('utf-8'))
			outFile.close()







