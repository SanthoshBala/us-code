from bs4 import BeautifulSoup, Comment, NavigableString
from lxml import etree
from string_utils import unescape
import time

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

xmlString = open("./data/olrc/archives/xhtml/1999/1999usc42.htm").read()
#for before, after in entities:
#    xmlString = xmlString.replace(before, after.encode('utf8'))

print time.time()
xmlSoup = BeautifulSoup(xmlString, "lxml")
xmlSoup.findAll(text=lambda text:isinstance(text, Comment))
print time.time()
parser = etree.XMLParser(remove_comments=True, recover=True)
lxmlTree = etree.parse("./data/olrc/archives/xhtml/1999/1999usc42.htm", parser)
print time.time()