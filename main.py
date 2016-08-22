#! /usr/bin/python

# main.py
#
# This file is meant for the highest-level functions which
# produce the final artifacts of this U.S. Code analysis project.

from olrc_client import *
from olrc_parser import *
import os

def buildReadableArchiveHtmlFiles():
	# Fetch XHTML Files
	client = OlrcClient()
	print "FETCHING ANNUAL ARCHIVES"
	client.fetchAllAnnualArchives()

	print "PARSING ANNUAL ARCHIVES"
	# For each year and title, parse it.
	for year, numTitles in OlrcClient.YEAR_TITLE_COUNT_MAP.items():

		print "%d" % year
		rawArchiveFileDir = client.OLRC_ROOT_DIRECTORY + "archives/%s/%d/" % (client.CODE_FORMAT_XHTML, year)
		prettyArchiveFileDir = "./archives/annual/%d/" % (year)
		# If prettyArchiveFileDir does not exist, create it.
		if not os.path.exists(prettyArchiveFileDir):
			os.makedirs(prettyArchiveFileDir)

		for title in range(1, numTitles + 1):
			print "\t%d" % title
			rawArchiveFileName = client.ARCHIVE_NAME_FORMAT_XHTML % (year, title)
			prettyArchiveFileName = "usc-%d-%d.html" % (year, title)

			parser = OlrcParser(rawArchiveFileDir + rawArchiveFileName)
			parser.parse(prettyArchiveFileDir + prettyArchiveFileName)

	return