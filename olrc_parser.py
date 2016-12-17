#!/usr/bin/python

# olrc_parser.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides all the utility necessary to parse and manipulator that data.

from bs4 import BeautifulSoup, Comment, NavigableString
from lxml import etree
from titlecase import titlecase
import time
import io
import re, htmlentitydefs
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

entities = [
    ('&nbsp;', u'\u00a0'),
    ('&acirc;', u'\u00e2'),
    ('&mdash;', u'\u2014'),
    ('&lsquo;', u'\u2018'),
    ('&rsquo;', u'\u2019'),
    ('&sect;', u'\u00A7'),
    ('&ldquo;', u'\u201C'),
    ('&rdquo;', u'\u201D'),
    ('&ndash;', u'\u2013'),
    ('&', u'\u0026'),
    ('<', u'\u003C'),
    ('>', u'\u003E'),
    ('&minus;', u'\u002D')
    ]
import fileinput

# Class for parsing OLRC data, based on BeautifulSoup.
class OlrcParser:

	# Annual Archive Code Formats
	CODE_FORMAT_GPO = "gpo"
	CODE_FORMAT_PDF = "pdf"
	CODE_FORMAT_XHTML = "xhtml"

	# Parser Types
	BS4_XML_PARSER = "lxml"
	BS4_PARSER = "bs4"
	LXML_PARSER = "lxml"

	def __init__(self, inFileName, format=CODE_FORMAT_XHTML):
		self.format = format
		self.parser = self.LXML_PARSER
		self.inFile = open(inFileName)
		
		#self.inFileRead = self.inFile.read()
		#for before, after in entities:
		#	self.inFileRead = self.inFileRead.replace(before, after.encode('utf-8'))
#		self.inFileRead = self._unescape(self.inFileRead.decode('utf-8'))

		return

	# Parse the file provided as input and write the output to outfile.
	def parse(self, outFileName):
		if self.parser == self.BS4_PARSER:
			if self.format == self.CODE_FORMAT_XHTML:
				self._sanitizeXML(outFileName)
			elif self.format == self.CODE_FORMAT_PDF:
				# TODO(santhoshbala): Write PDF parser.
				print "TODO(santhoshbala): Write PDF parser."
				pass
			else:
				# TODO(santhoshbala): Write GPO parser.
				print "TODO(santhoshbala): Write GPO parser."
				pass
		elif self.parser == self.LXML_PARSER:
			self._sanitizeXML(outFileName)

		for line in fileinput.FileInput(outFileName, inplace=1):
			if line.rstrip():
				print line

		return

	def _sanitizeXML(self, outFileName):
		
		start = time.time()
		if self.parser == self.BS4_PARSER:
			xmlSoup = BeautifulSoup(self.inFile, BS4_XML_PARSER)

			self._deleteEditorialNotes(xmlSoup)
			self._deleteInlineStyles(xmlSoup)
			self._injectStyleSheet(xmlSoup)
			self._injectMetaViewportTag(xmlSoup)
			self._titleCaseTitleAndChapter(xmlSoup)
			self._dotSectionHeaders(xmlSoup)
			self._removeSourceParentheses(xmlSoup)

			outFile = open(outFileName, 'w')
			outFile.write(xmlSoup.prettify("utf-8"))
			outFile.close()
		elif self.parser == self.LXML_PARSER:
			# Set recover=True so that parser doesn't fail on encountering
			# HTML entities like &mdash;
			#lxmlParser = etree.XMLParser(remove_comments=True, resolve_entities=False)
			lxmlParser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
			lxmlTree = etree.parse(self.inFile, lxmlParser)
			#lxmlTree = self._removeNamespaces(lxmlTree)
			self._deleteEditorialNotes(lxmlTree)
			self._deleteInlineStyles(lxmlTree)
			self._injectStyleSheet(lxmlTree)
			self._injectMetaViewportTag(lxmlTree)
			self._titleCaseTitleAndChapter(lxmlTree)
			self._dotSectionHeaders(lxmlTree)
			self._removeSourceParentheses(lxmlTree)
			lxmlTree.write(outFileName, pretty_print=True)

		print "\t\t%f" % (time.time() - start)

		return

	def _injectMetaViewportTag(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			head = xmlSoup.find("head")
			mvt = etree.SubElement(head, "meta",
									attrib={"content":"width=device-width, initial-scale=1"})

		if self.parser == self.BS4_PARSER:
			head = xmlSoup.find("head")
			metaTag = xmlSoup.new_tag("meta", content="width=device-width, initial-scale=1")
			metaTag.attrs['name'] = "viewport"
			head.insert(2, metaTag)

		return

	def _removeSourceParentheses(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			sourceCredits = xmlSoup.findall("//p[@class='source-credit']")
			for sourceCredit in sourceCredits:
				# Strip parentheses and new lines
				sourceCredit.text = sourceCredit.text.strip()[1:-1]
		if self.parser == self.BS4_PARSER:
			sourceCredits = xmlSoup.findAll("p", {"class" : "source-credit"})
			for sourceCredit in sourceCredits:
				# Strip parentheses and new lines
				sourceCredit.string = sourceCredit.text.strip()[1:-1]

		return

	def _dotSectionHeaders(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			sectionHeaders = xmlSoup.findall("//h3[@class='section-head']")
			for sectionHeader in sectionHeaders:
				# Replace period with middle dot (only first instance)
				sectionHeader.text = sectionHeader.text.replace(u".", u" \u00B7", 1)
		if self.parser == self.BS4_PARSER:
			sectionHeaders = xmlSoup.findAll("h3", {"class" : "section-head"})
			for sectionHeader in sectionHeaders:
				# Replace period with middle dot (only first instance)
				sectionHeader.string = sectionHeader.text.replace(u".", u" \u00B7", 1)

		return

	def _titleCaseTitleAndChapter(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			titles = xmlSoup.findall("//h1[@class='usc-title-head']")
			for title in titles:
				title.text = u" \u2014 ".join([titlecase(s.lower()) for s in title.text.split(u"\u2014")])

			chapters = xmlSoup.findall("//h3[@class='chapter-head']")
			for chapter in chapters:
				# Clean em dash and title case
				chapter.text = u". ".join([titlecase(s.lower()) for s in chapter.text.split(u"\u2014")])

			subchapters = xmlSoup.findall("//h3[@class='subchapter-head']")
			for subchapter in subchapters:
				# Clean em dash and title case
				if u"\u2014" in subchapter.text:
					[prefix, suffix] = subchapter.text.split(u"\u2014", 1)
					[heading, number] = prefix.split(" ", 1)
					heading = titlecase(heading.lower())
					suffix = titlecase(suffix.lower())
					subchapter.text = u"%s %s\u2014%s" % (heading, number, suffix)
				else:
					subchapter.text = titlecase(subchapter.text.lower())

		if self.parser == self.BS4_PARSER:
			titles = xmlSoup.findAll("h1", {"class" : "usc-title-head"})
			for title in titles:
				# Clean em dash and title case
				title.string = u" \u2014 ".join([titlecase(s.lower()) for s in title.text.split(u"\u2014")])	

			chapters = xmlSoup.findAll("h3", {"class" : "chapter-head"})
			for chapter in chapters:
				# Clean em dash and title case
				chapter.string = u". ".join([titlecase(s.lower()) for s in chapter.text.split(u"\u2014")])

			subchapters = xmlSoup.findAll("h3", {"class" : "subchapter-head"})

			for subchapter in subchapters:
				# Clean em dash and title case
				if u"\u2014" in subchapter.text:
					[prefix, suffix] = subchapter.text.split(u"\u2014", 1)
					[heading, number] = prefix.split(" ", 1)
					heading = titlecase(heading.lower())
					suffix = titlecase(suffix.lower())
					subchapter.string = u"%s %s\u2014%s" % (heading, number, suffix)
				else:
					subchapter.string = titlecase(subchapter.text.lower())
		
		return

	def _injectStyleSheet(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			head = xmlSoup.find("head")
			stylesheet = etree.SubElement(head, "link",
											attrib={"rel":"stylesheet",
											"type":"text/css",
											"href":"../../stylesheets/us-code-title.css"})
				
		if self.parser == self.BS4_PARSER:
			head = xmlSoup.find("head")
			linkTag = xmlSoup.new_tag("link", rel="stylesheet", type="text/css", href="../../stylesheets/us-code-title.css")
			head.insert(1, linkTag)

		return

	# Delete all inline styles to prepare for injecting new styles.
	def _deleteInlineStyles(self, xmlSoup):
		if self.parser == self.LXML_PARSER:
			lxmlTree = xmlSoup
			for child in lxmlTree.iter():
				child.attrib.pop('style', None)
				child.attrib.pop('width', None)
				
		if self.parser == self.BS4_PARSER:
			for tag in xmlSoup.recursiveChildGenerator():
				try:
					tag.attrs.pop('style', None)
					tag.attrs.pop('width', None)
				except AttributeError:
					pass

		return

	# By default, parsing via LXML will leave namespace delcarations in
	# the document. To simplify parsing, remove these.
	def _removeNamespaces(self, lxmlTree):
		xslt = '''<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
				<xsl:output method="xml" indent="no"/>

				<xsl:template match="/|comment()|processing-instruction()">
				    <xsl:copy>
				      <xsl:apply-templates/>
				    </xsl:copy>
				</xsl:template>

				<xsl:template match="*">
				    <xsl:element name="{local-name()}">
				      <xsl:apply-templates select="@*|node()"/>
				    </xsl:element>
				</xsl:template>

				<xsl:template match="@*">
				    <xsl:attribute name="{local-name()}">
				      <xsl:value-of select="."/>
				    </xsl:attribute>
				</xsl:template>
				</xsl:stylesheet>
				'''
		xsltDoc = etree.parse(io.BytesIO(xslt))
		transform = etree.XSLT(xsltDoc)
		lxmlTree = transform(lxmlTree)

		return lxmlTree

	##
	# Removes HTML or XML character references and entities from a text string.
	#
	# @param text The HTML (or XML) source text.
	# @return The plain text, as a Unicode string, if necessary.

	def _unescape(self, text):
	    def fixup(m):
	        text = m.group(0)
	        if text[:2] == "&#":
	            # character reference
	            try:
	                if text[:3] == "&#x":
	                    return unichr(int(text[3:-1], 16))
	                else:
	                    return unichr(int(text[2:-1]))
	            except ValueError:
	                pass
	        else:
	            # named entity
	            try:
	                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
	            except KeyError:
	                pass
	        return text # leave as is
	    return re.sub("&#?\w+;", fixup, text, flags=re.UNICODE)

	# USC XML files contain a variety of editorial notes, including notes about
	# (1) amendments
	# (2) notes about other sections which refer to the current section
	# (3) cross-references to other legal documents
	# (4) other miscellaneous notes
	# (5) <script>, <br>, etc.
	def _deleteEditorialNotes(self, xmlSoup):
		# To get rid of all notes, need to delete <table>, <div>, <p>, <h4>, and <!--> tags.
		tableClasses = set(["uscdispo3col", "uscdispo2col", "uschistrev"])
		h3Classes = set([]) # "analysis-subhead"
		h4Classes = set(["note-head", "note-sub-head", "source-credit", "analysis-subhead", "futureamend-note-head"])
		pClasses = set(["note-head", "note-body", "note-body-1em", "footnote", "presidential-signature",
					"note-body-flush0_hang1", "note-body-block", "note-body-2em", "note-body-flush2_hang3",
					"futureamend-note-body", "note-body-flush3_hang4", "note-body-flush0_hang4",
					"note-body-3em"])
		divClasses = set(["analysis", "two-column-analysis-style-content-right"])
		divIds = set(["footer", "resizeWindow", "menu", "menu_homeLink", "header"])
		spanIds = set(["resizeWindow"])
		deletableTags = set(["br", "meta", "script", "noscript", "link", "sup"])
		nsExtraneousTags = set(["{http://www.w3.org/1999/xhtml}strong", 
								"{http://www.w3.org/1999/xhtml}cap-smallcap", 
								"{http://www.w3.org/1999/xhtml}em"])
		extraneousTags = set(["strong", "cap-smallcap", "em"])
		commentTypes = set(["notes", "repeal-note", "secref", "sectionreferredto", "amendment-note", 
						"crossreference-note", "miscellaneous-note", "sourcecredit",
						"footnote", "analysis", "effectivedate-note", "documentid",
						"PDFPage", "usckey", "itemsortkey", "itempath:", "HTTP",
						"referenceintext-note", "changeofname-note", "shorttitle-note",
						"function-transfer-repeal-savingsclause-similarprovisions-note",
						"savings-provision-note", "repeal-savingsprovision-note", "repealsummary",
						"codification-note", "priorprovisions-note", "constitutionalprovisions-note",
						"function-transfer-note", "effectivedate-terminationdate-note",
						"historicalandrevision-note", "terminationdate-note", "construction-note"])

		if self.parser == self.LXML_PARSER:
			lxmlTree = xmlSoup
			root = lxmlTree.getroot()
			removableNodes = set()
			for child in lxmlTree.iter():
				# HTML entities like &mdash are independent children in
				# the tree, and have type "cython_function_or_method".
				# Skip them.
				if type(child.tag).__name__ == 'cython_function_or_method':	
					continue					

				# Strip namespace declaration from tag name	
				tagName = child.tag

				if tagName == "table":
				 	if child.attrib.get('class') in tableClasses:
				 		removableNodes.add(child)
				elif tagName == "h3":
				 	if child.attrib.get('class') in h3Classes:
				 		removableNodes.add(child)
				elif tagName == "h4":
					if child.attrib.get('class') in h4Classes:
						removableNodes.add(child)
				elif tagName == "p":
					if child.attrib.get('class') in pClasses:
						removableNodes.add(child)
				elif tagName == "div":
					if child.attrib.get('class') in divClasses:
						removableNodes.add(child)
				 	if child.attrib.get('id') in divIds:
				 		removableNodes.add(child)
				elif tagName == "span":
					if child.attrib.get('id') in spanIds:
						removableNodes.add(child)
				elif tagName in deletableTags:
					removableNodes.add(child)
			
			for node in removableNodes:
				node.getparent().remove(node)

			for extraneousTag in extraneousTags:
				etree.strip_tags(lxmlTree, extraneousTag)

		elif self.parser == self.BS4_PARSER:
			commentTags = xmlSoup.findAll(text=lambda text:isinstance(text, Comment))

			loopStart = time.time()
			for comment in commentTags:
				for commentType in commentTypes:
					if commentType in comment:
						comment.extract()

			tags = xmlSoup.findAll(True)
			decomposeSet = set()
			for tag in tags:
				if tag.name == "table":
					if tag.attrs.get('class'):
						if tag.attrs.get('class')[0] in tableClasses:
							tag.extract()
				elif tag.name == "h3":
					if tag.attrs.get('class'):
					 	if tag.attrs.get('class')[0] in h3Classes:
							tag.extract()
				elif tag.name == "h4":
					if tag.attrs.get('class'):
						if tag.attrs.get('class')[0] in h4Classes:
							tag.extract()
				elif tag.name == "p":
					if tag.attrs.get('class'):
						if tag.attrs.get('class')[0] in pClasses:
							tag.extract()
				elif tag.name == "div":
					if tag.attrs.get('class'):
						if tag.attrs.get('class')[0] in divClasses:
							tag.extract()
					if tag.attrs.get('id'):
						if tag.attrs.get('id') in divIds:
							tag.extract()
				elif tag.name == "span":
					if tag.attrs.get('id'):
						if tag.attrs.get('id') in spanIds:
							tag.extract()
				elif tag.name in deletableTags:
					tag.extract()
				elif tag.name in extraneousTags:
					tag.replaceWith(NavigableString(tag.text))
