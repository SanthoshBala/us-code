#!/usr/bin/python

# olrc_parser.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides all the utility necessary to parse and manipulator that data.

from bs4 import BeautifulSoup, Comment
from titlecase import titlecase

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

		print "_deleteEditorialNotes"
		self._deleteEditorialNotes(xmlSoup)
		print "_deleteInlineStyles"
		self._deleteInlineStyles(xmlSoup)
		print "_injectStyleSheet"
		self._injectStyleSheet(xmlSoup)
		print "_injectMetaViewportTag"
		self._injectMetaViewportTag(xmlSoup)
		print "_titleCaseTitleAndChapter"
		self._titleCaseTitleAndChapter(xmlSoup)
		print "_dotSectionHeaders"
		self._dotSectionHeaders(xmlSoup)
		print "_removeSourceParentheses"
		self._removeSourceParentheses(xmlSoup)

		outFile = open(outFileName, 'w')
		outFile.write(xmlSoup.prettify("utf-8"))
		outFile.close()

		return

	def _injectMetaViewportTag(self, xmlSoup):
		head = xmlSoup.find("head")
		metaTag = xmlSoup.new_tag("meta", content="width=device-width, initial-scale=1")
		metaTag.attrs['name'] = "viewport"
		head.insert(2, metaTag)

		return

	def _removeSourceParentheses(self, xmlSoup):
		sourceCredits = xmlSoup.findAll("p", {"class" : "source-credit"})

		for sourceCredit in sourceCredits:
			# Strip parentheses and new lines
			sourceCredit.string = sourceCredit.text.strip()[1:-1]

		return

	def _dotSectionHeaders(self, xmlSoup):
		sectionHeaders = xmlSoup.findAll("h3", {"class" : "section-head"})

		for sectionHeader in sectionHeaders:
			# Replace period with middle dot
			sectionHeader.string = sectionHeader.text.replace(u".", u" \u00B7")

		return

	def _titleCaseTitleAndChapter(self, xmlSoup):
		titles = xmlSoup.findAll("h1", {"class" : "usc-title-head"})

		for title in titles:
			# Clean em dash
			title.string = title.text.replace(u"\u2014", u" \u2014 ")
			# Title case
			title.string = titlecase(title.text.lower())

		chapters = xmlSoup.findAll("h3", {"class" : "chapter-head"})

		for chapter in chapters:
			# Clean em dash
			chapter.string = chapter.text.replace(u"\u2014", u". ")
			# Title case
			chapter.string = titlecase(chapter.text.lower())
		
		return

	def _injectStyleSheet(self, xmlSoup):
		head = xmlSoup.find("head")
		linkTag = xmlSoup.new_tag("link", rel="stylesheet", type="text/css", href="us-code-title.css")
		head.insert(1, linkTag)

		return

	# Delete all inline styles to prepare for injecting new styles.
	def _deleteInlineStyles(self, xmlSoup):
		for tag in xmlSoup.recursiveChildGenerator():
			try:
				tag.attrs.pop('style', None)
				tag.attrs.pop('width', None)
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
		h3Classes = ["analysis-subhead"]
		h4Classes = ["note-head", "note-sub-head", "source-credit", "analysis-subhead"]
		pClasses = ["note-head", "note-body", "note-body-1em", "footnote", "presidential-signature",
					"note-body-flush0_hang1", "note-body-block", "note-body-2em"]
		divClasses = ["analysis"]
		divIds = ["footer", "resizeWindow", "menu", "menu_homeLink", "header"]
		spanIds = ["resizeWindow"]
		deletableTags = ["br", "meta", "script", "noscript", "link", "sup"]
		extraneousTags = ["strong"]
		commentTypes = ["notes", "repeal-note", "secref", "sectionreferredto", "amendment-note", 
						"crossreference-note", "miscellaneous-note", "source-credit",
						"footnote", "analysis", "effectivedate-note", "documentid:",
						" PDFPage", "usckey:", "itemsortkey:", "itempath:", "HTTP",
						"referenceintext-note", "changeofname-note", "shorttitle-note",
						"function-transfer-repeal-savingsclause-similarprovisions-note"]

		for tableClass in tableClasses:
			tags = xmlSoup.findAll("table", {"class" : tableClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for hClass in h3Classes:
			tags = xmlSoup.findAll("h3", {"class" : hClass})
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for hClass in h4Classes:
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

		for deletableTag in deletableTags:
			tags = xmlSoup.findAll(deletableTag)
			for tag in tags:
				try:
					tag.extract()
				except AttributeError:
					pass

		for extraneousTag in extraneousTags:
			tags = xmlSoup.findAll(extraneousTag)
			for tag in tags:
				tag.replaceWith(tag.text)

		return