#!/usr/bin/python

# olrc_parser.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides all the utility necessary to parse and manipulator that data.

from bs4 import BeautifulSoup

# Class for parsing OLRC data, based on BeautifulSoup.
class OlrcParser:

	# Annual Archive Code Formats
	CODE_FORMAT_GPO = "gpo"
	CODE_FORMAT_PDF = "pdf"
	CODE_FORMAT_XHTML = "xhtml"

	# Parser Types
	XML_PARSER = "lxml"

	def __init__(self, inFileName, format=CODE_FORMAT_XHTML):
		self.format = format
		self.inFile = open(inFileName)

		return

	# Parse the file provided as input and write the output to outfile.
	def parse(self, outFileName):
		if self.format == self.CODE_FORMAT_XHTML:
			self._parseXML(outFileName)
		elif self.format == self.CODE_FORMAT_PDF:
			# TODO(santhoshbala): Write PDF parser.
			pass
		else:
			# TODO(santhoshbala): Write GPO parser.
			pass

		return

	def _parseXML(self, outFileName):
		

		self._deleteXmlHeaderUI(xmlSoup)

		self._deleteXmlMenu(xmlSoup)

		outFile = open(outFileName, 'w')

		return

	# USC XML files contain header UI at the top of the document.
	# Delete that UI for the sake of removing non-code text.
	def _deleteXmlHeaderUI(self, xmlSoup):
		header = xmlSoup.find("div", {"id" : "header"})
		header.extract()

		return

	# USC XML files contain a menu UI at the top of the document.
	# Delete that UI for the sake of removing non-code text.
	def _deleteXmlMenu(self, xmlSoup):
		menu = xmlSoup.find("div", {"id" : "menu"})
		menu.extract()

		return

	# USC XML files contain a hidden resizeWindow div.
	# Delete that div for the sake of clarity.
	def _deleteXmlResizeWindow(self, xmlSoup):
		resizeWindowDiv = xmlSoup.find("div", {"id" : "resizeWindow"})
		resizeWindowDiv.extract()

		resizeWindowSpan = xmlSoup.find("span", {"id" : "resizeWindow"})
		resizeWindowSpan.extract()

		return

	def _deleteXmlFooter(self, xmlSoup):
		footer = xmlSoup.find("div", {"id" : "footer"})
		footer.extract()

		return

	# USC XML files contain XML comments indicating where pagebreaks
	# would occur in the corresponding PDF version.
	# Delete these comments to minimize unnecessary diffs, because
	# the positions of these breaks certainly change over time.
	def _deletePdfPageBreaks(self, xmlSoup):
		pageBreaks = xmlSoup.findAll(text=lambda text:isinstance(text, Comment) and " PDFPage" in text)
		for pageBreak in pageBreaks:
			pageBreak.extract()

		return