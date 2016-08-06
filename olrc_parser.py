#!/usr/bin/python

# olrc_parser.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides all the utility necessary to parse and manipulator that data.

from bs4 import BeautifulSoup, Comment

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
			self._sanitizeXML(outFileName)
		elif self.format == self.CODE_FORMAT_PDF:
			# TODO(santhoshbala): Write PDF parser.
			pass
		else:
			# TODO(santhoshbala): Write GPO parser.
			pass

		return

	def _sanitizeXML(self, outFileName):
		
		xmlSoup = BeautifulSoup(self.inFile, OlrcParser.XML_PARSER)

		self._deleteEditorialNotes(xmlSoup)
		self._deleteInlineStyles(xmlSoup)

		outFile = open(outFileName, 'w')
		outFile.write(xmlSoup.prettify("utf-8"))
		outFile.close()

		return

	# Delete all inline styles to prepare for injecting new styles.
	def _deleteInlineStyles(self, xmlSoup):
		for tag in xmlSoup.recursiveChildGenerator():
			try:
				tag.attrs['style'] = None
			except AttributeError:
				pass

		return

	# USC XML files contain a variety of editorial notes, including notes about
	# (1) amendments
	# (2) notes about other sections which refer to the current section
	# (3) cross-references to other legal documents
	# (4) other miscellaneous notes
	# (5) <script>, <br>, etc.
	def _deleteEditorialNotes(self, xmlSoup):
		# To get rid of all notes, need to delete <table>, <div>, <p>, <h4>, and <!--> tags.
		tableClasses = ["uscdispo3col"]
		hClasses = ["note-head", "note-sub-head", "source-credit"]
		pClasses = ["note-head", "note-body", "note-body-1em", "footnote", "presidential-signature"]
		divClasses = ["analysis"]
		divIds = ["footer", "resizeWindow", "menu", "menu_homeLink", "header"]
		spanIds = ["resizeWindow"]
		tagTypes = ["br", "meta", "script", "noscript", "link"]
		commentTypes = ["notes", "repeal-note", "secref", "sectionreferredto", "amendment-note", 
						"crossreference-note", "miscellaneous-note", "source-credit",
						"footnote", "analysis", "effectivedate-note", "documentid:",
						" PDFPage", "usckey:", "itemsortkey:", "itempath:", "HTTP"]

		for tableClass in tableClasses:
			tags = xmlSoup.findAll("table", {"class" : tableClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for hClass in hClasses:
			tags = xmlSoup.findAll("h4", {"class" : hClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for pClass in pClasses:
			tags = xmlSoup.findAll("p", {"class" : pClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for divClass in divClasses:
			tags = xmlSoup.findAll("div", {"class" : divClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for divId in divIds:
			tags = xmlSoup.findAll("div", {"id" : divId})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for spanId in spanIds:
			tags = xmlSoup.findAll("span", {"id" : spanId})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for commentType in commentTypes:
			tags = xmlSoup.findAll(text=lambda text:isinstance(text, Comment) and commentType in text)
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for tagType in tagTypes:
			tags = xmlSoup.findAll(tagType)
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		return