#! /usr/bin/python

# main.py
#
# This file is meant for the highest-level functions which
# produce the final artifacts of this U.S. Code analysis project.

from olrc_client import *
from olrc_parser import *
from olrc_differ import *
import os
import time

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
			print "\tTitle %d" % title
			rawArchiveFileName = client.ARCHIVE_NAME_FORMAT_XHTML % (year, title)
			prettyArchiveFileName = "usc-%d-%02d.html" % (year, title)

			parser = OlrcParser(rawArchiveFileDir + rawArchiveFileName)
			parser.parse(prettyArchiveFileDir + prettyArchiveFileName)

	return

def buildAnnualDiffHtmlFiles():
	print "BUILDING ANNUAL DIFF FILES"
	for year, numTitles in OlrcClient.YEAR_TITLE_COUNT_MAP.items():
		# For each year up to second to last...
		if year == OlrcClient.FIRST_ANNUAL_ARCHIVE_YEAR:
			continue

		postYear = year
		preYear = year - 1
		
		print "%d -> %d" % (preYear, postYear)

		preYearFileDir = "./archives/annual/%d/" % (preYear)
		postYearFileDir = "./archives/annual/%d/" % (postYear)
		if OlrcDiffer.DIFF_METHOD == OlrcDiffer.METHOD_HTML_DIFF:
			annualDiffFileDir = "./archives/html_diff/%d/" % (postYear)
		elif OlrcDiffer.DIFF_METHOD == OlrcDiffer.METHOD_HTML_ANNOTATE:
			annualDiffFileDir = "./archives/html_annotate/%d/" % (postYear)

		# If annualDiffFileDir does not exist, create it.
		if not os.path.exists(annualDiffFileDir):
			os.makedirs(annualDiffFileDir)

		for title in range(1, numTitles + 1):
			start = time.time()
			# Confirm that this title exists in the previous year.
			if title > OlrcClient.YEAR_TITLE_COUNT_MAP[preYear]:
				continue

			print "\tTitle %d" % title
			# Get filenames for each title.
			preTitleFileName = "usc-%d-%02d.html" % (preYear, title)
			postTitleFileName = "usc-%d-%02d.html" % (postYear, title)
			titleDiffFileName = "usc-%d-%02d-diff.html" % (postYear, title)

			differ = OlrcDiffer(preYearFileDir + preTitleFileName, 
									postYearFileDir + postTitleFileName)
			differ.write(annualDiffFileDir + titleDiffFileName)
			print "\t\t%f" % (time.time() - start)

	return

def injectAnnualDiffStyles():
	print "INJECTING ANNUAL DIFF STYLES"
	for year, numTitles in OlrcClient.YEAR_TITLE_COUNT_MAP.items():
		# For each year up to second to last...
		if year == OlrcClient.FIRST_ANNUAL_ARCHIVE_YEAR:
			continue

		postYear = year
		preYear = year - 1
		
		print "%d -> %d" % (preYear, postYear)

		preYearFileDir = "./archives/annual/%d/" % (preYear)
		postYearFileDir = "./archives/annual/%d/" % (postYear)
		if OlrcDiffer.DIFF_METHOD == OlrcDiffer.METHOD_HTML_DIFF:
			annualDiffFileDir = "./archives/html_diff/%d/" % (postYear)
		elif OlrcDiffer.DIFF_METHOD == OlrcDiffer.METHOD_HTML_ANNOTATE:
			annualDiffFileDir = "./archives/html_annotate/%d/" % (postYear)

		for title in range(1, numTitles + 1):
			start = time.time()
			# Confirm that this title exists in the previous year.
			if title > OlrcClient.YEAR_TITLE_COUNT_MAP[preYear]:
				continue

			print "\tTitle %d" % title
			# Get filenames for each title.
			titleDiffFileName = "usc-%d-%02d-diff.html" % (postYear, title)
			lxmlParser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
			lxmlTree = etree.parse(titleDiffFileName, lxmlParser)

			# Inject Meta Viewport Tag
			head = lxmlTree.find("head")
			mvt = etree.SubElement(head, "meta",
									attrib={"content":"width=device-width, initial-scale=1"})
			# Inject Style Sheet
			stylesheet = etree.SubElement(head, "link",
											attrib={"rel":"stylesheet",
											"type":"text/css",
											"href":"../../../explorer/stylesheets/us-code-title-diff.css"})
			print "\t\t%f" % (time.time() - start)

	return