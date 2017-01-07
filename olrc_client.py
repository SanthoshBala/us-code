#!/usr/bin/python

# olrc-client.py
#
# The OLRC (Office of the Law Revision Counsel) maintains the U.S. Code and
# Public Laws. They publish data in a variety of formats, but this class
# provides all the utility necessary to fetch US Code data.

import httplib
import os
from subprocess import call
from urllib2 import urlopen

# Class for communicating with OLRC to download U.S. Code data.
class OlrcClient:
	def __init__(self):
		# Root directory for downloading and organizing files.
		self.OLRC_ROOT_DIRECTORY = "./data/olrc/"

	# The Annual Historical Archives are available from 1994 - 2015.
	FIRST_ANNUAL_ARCHIVE_YEAR = 1994
	LAST_ANNUAL_ARCHIVE_YEAR = 2015

	# Annual Archive Code Formats
	CODE_FORMAT_GPO = "gpo"
	CODE_FORMAT_PDF = "pdf"
	CODE_FORMAT_XHTML = "xhtml"	

	ARCHIVE_NAME_FORMAT_PDF = "%dusc%02d.pdf"
	ARCHIVE_NAME_FORMAT_XHTML = "%dusc%02d.htm"

	# The Annual Archives are available in three formats: PDF, GPO, and XHTML.
	# Find the raw archive files at the following URLs.
	# Base URL: http://uscode.house.gov/download/annualhistoricalarchives/...
	# 	GPO: ...downloadGPO.shtml
	# 	PDF: ...downloadPDF.shtml
	# 	XHTML: ...downloadxhtml.shtml
	TITLE_ARCHIVE_FORMAT_URL_MAP = {
		# (%d, %d) = (YEAR, TITLE)
		CODE_FORMAT_GPO : "http://uscode.house.gov/download/annualhistoricalarchives/zip/%d/usc%02d.zip",
		# (%d, %d, %d) = (YEAR, YEAR, TITLE)
		CODE_FORMAT_PDF : "http://uscode.house.gov/download/annualhistoricalarchives/pdf/%d/%dusc%02d.pdf",
		# (%d, %d, %d) = (YEAR, YEAR, TITLE)
		CODE_FORMAT_XHTML : "http://uscode.house.gov/download/annualhistoricalarchives/XHTML/%d/%dusc%02d.htm"
	}

	# The U.S. Code has had a variable number of titles between 1994 and 2015.
	# Encode the number of titles for ease of code parsing. {1994:50} signifies
	# that there were 50 titles in the U.S. Code in 1994.
	YEAR_TITLE_COUNT_MAP = {
		1994 : 50,
		1995 : 50,
		1996 : 50,
		1997 : 50,
		1998 : 50,
		1999 : 50,
		2000 : 50,
		2001 : 50,
		2002 : 50,
		2003 : 50,
		2004 : 50,
		2005 : 50,
		2006 : 50,
		2007 : 50,
		2008 : 50,
		2009 : 50,
		2010 : 50,
		2011 : 51,
		2012 : 51,
		2013 : 51,
		2014 : 54,
		2015 : 54,
		2016 : 54
	}

	# For any functions which require a year as an input, use this internal
	# function to validate that the year is within the proper bounds.
	def _isValidYear(self, year):
		if (year < OlrcClient.FIRST_ANNUAL_ARCHIVE_YEAR) or \
			(year > OlrcClient.LAST_ANNUAL_ARCHIVE_YEAR):
			return False
		else:
			return True

	# For any files that need to be downloaded from the web, use this internal
	# function to save the contents of the file locally.
	def _downloadWebDocument(self, webUrl, destDir):
		fileName = webUrl.split("/")[-1]
		cmd = "curl --create-dirs -# -o %s%s %s" % (destDir, fileName, webUrl)
		call(cmd, shell=True)

		return

	def fetchAnnualArchiveTitle(self, title, year=LAST_ANNUAL_ARCHIVE_YEAR,
		format=CODE_FORMAT_XHTML):

		baseDownloadUrl = OlrcClient.TITLE_ARCHIVE_FORMAT_URL_MAP[format]
		destDir = self.OLRC_ROOT_DIRECTORY + "archives/%s/%d/" % (format, year)
		# If destDir does not exist, create it.
		if not os.path.exists(destDir):
			os.makedirs(destDir)

		# If file already exists, continue.
		existingFiles = os.listdir(destDir)
		# TODO(santhoshbala): Generalize this condition to work for non-XHTML file formats.
		if OlrcClient.ARCHIVE_NAME_FORMAT_XHTML % (year, title) in existingFiles:
			pass
		else:
			if format == OlrcClient.CODE_FORMAT_GPO:
				downloadUrl = baseDownloadUrl % (year, title)
			else:
				downloadUrl = baseDownloadUrl % (year, year, title)

			self._downloadWebDocument(downloadUrl, destDir)

		return

	def fetchAnnualArchive(self, year=LAST_ANNUAL_ARCHIVE_YEAR, 
								format=CODE_FORMAT_XHTML):
		# Validate year.
		if not self._isValidYear(year):
			return None

		# Download all titles for this year.
		numTitles = OlrcClient.YEAR_TITLE_COUNT_MAP[year]
		
		for title in range(1, numTitles + 1):
			self.fetchAnnualArchiveTitle(title, year, format)

		return

	def fetchAllAnnualArchives(self, format=CODE_FORMAT_XHTML):
		# Download archives for all years.
		for year in range(OlrcClient.FIRST_ANNUAL_ARCHIVE_YEAR,
							OlrcClient.LAST_ANNUAL_ARCHIVE_YEAR + 1):
			self.fetchAnnualArchive(year=year, format=format)

		return

	# Change root directory for downloading and organizing files.
	def setRootDirectory(self, olrcRootDir):
		self.OLRC_ROOT_DIRECTORY = olrcRootDir
		return
