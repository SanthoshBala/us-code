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
		
		xmlSoup = BeautifulSoup(self.inFile, OlrcParser.XML_PARSER)
		self._deleteXmlHeaderUI(xmlSoup)

		self._deleteXmlMenu(xmlSoup)
		self._deleteXmlResizeWindow(xmlSoup)

		outFile = open(outFileName, 'w')
		outFile.write(xmlSoup.prettify("utf-8"))
		outFile.close()

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
		try:
			resizeWindowDiv.extract()
		except AttributeError:
			pass

		resizeWindowSpan = xmlSoup.find("span", {"id" : "resizeWindow"})
		try:
			resizeWindowSpan.extract()
		except AttributeError:
			pass

		return

	# Delete footer XML for sake of clarity.
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

	# USC XML files contain a variety of editorial notes, including notes about
	# (1) amendments
	# (2) notes about other sections which refer to the current section
	# (3) cross-references to other legal documents
	# (4) other miscellaneous notes
	def _deleteEditorialNotes(self, xmlSoup):
		# To get rid of all notes, need to delete classes matching "note-head"
		# and "note-body", as well as the comments for "repeal-note", "secref",
		# "sectionreferredto", "amendment-note", "crossreference-note", and
		# "miscellaneous-note".
		pClasses = ["note-head", "note-body"]
		commentTypes = ["repeal-note", "secref", "sectionreferredto", "amendment-note", 
						"crossreference-note", "miscellaneous-note"]

		for pClass in pClasses:
			tags = xmlSoup.findAll("p", {"class" : pClass})
			for tag in tags:
				try:
					print pClass
					tag.extract()
				except AttributeError:
					pass

		for commentType in commentTypes:
			tags = xmlSoup.findAll(text=lambda text:isinstance(text, Comment) and commentType in text)
			for tag in tags:
				try:
					print commentType
					tag.extract()
				except AttributeError:
					pass

		return