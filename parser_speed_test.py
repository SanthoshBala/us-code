from bs4 import BeautifulSoup, Comment, NavigableString
from lxml import etree
from string_utils import unescape
import time
import io

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

pClasses = set(["note-head", "note-body", "note-body-1em", "footnote", "presidential-signature",
                    "note-body-flush0_hang1", "note-body-block", "note-body-2em", "note-body-flush2_hang3",
                    "futureamend-note-body", "note-body-flush3_hang4", "note-body-flush0_hang4",
                    "note-body-3em"])
        

xmlString = open("./data/olrc/archives/xhtml/1999/1999usc42.htm").read()
#for before, after in entities:
#    xmlString = xmlString.replace(before, after.encode('utf8'))

print time.time()
#xmlSoup = BeautifulSoup(xmlString, "lxml")
#xmlSoup.findAll(text=lambda text:isinstance(text, Comment))
print time.time()
parser = etree.XMLParser(remove_comments=True, recover=True, remove_pis=True, ns_clean=True)
lxmlTree = etree.parse("./data/olrc/archives/xhtml/1995/1995usc01.htm", parser)

#for child in lxmlTree.getroot():
#    if child.tag.split("}")[1] == "emph":
#        print type(child), child.tag, child.attrib.get('class'), child.text

#for child in dom.getroot():
#    print type(child), child.tag, child.attrib.get('class'), child.text

print time.time()