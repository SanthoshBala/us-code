from flask import Flask, render_template
from database import *
from datetime import datetime
import os
import tarfile

app = Flask(__name__)



@app.route('/')
def home():
    """Return homepage."""
    return render_template('index.html')

@app.route('/compress')
def compressCodeTitleTemplates():
    """Compress US Code Title templates."""
    # os.chdir("./templates/preambles")
    filesToCompress = os.listdir("./templates/preambles")
    # filesToCompress = os.listdir("./static/js")
    # filesToCompress = os.listdir("./static/js/")
    # filesToCompress = os.listdir("./static/preambles/")

    # Create tarfile.
    tar = tarfile.open("templates/preambles/preambles.tar.gz", "w|gz")
    for filename in filesToCompress:
     	tar.add(filename)
     	# Remove original files
     	os.remove(filename)

    tar.close()

    # return render_template('index.html')
    return render_template('index.html')

@app.route('/archive/annual/<int:year>/<string:title>')
def yearTitleArchive(year, title):
	"""Return styled annual archive."""
	
	data = {
		"annual" : {},
		"congressional" : {},
		"titular" : {}
	}

	# Given year, find relevant Congresses.
	congresses = set()
	for congress, senate in SENATES.iteritems():
		if year >= senate.first_year and year <= senate.last_year:
			congresses.add(senate.ordinality)

	# Given congresses, find all leaders and publicLaws they passed in year.
	for congress in congresses:
		enactedLaws = []
		for publicLawId, publicLaw in PUBLIC_LAWS[congress].iteritems():
			if publicLaw.date_enacted.split()[-1] == str(year) and int(title) in publicLaw.amended_titles:
				enactedLaws.append(publicLaw)

		enactedLaws.sort(key = lambda x: datetime.strptime(x.date_enacted, '%B %d, %Y'))

		leaders = {
			"president" : PRESIDENTS[YEARS[year]["president"]],
			"houseDemLeader" : LEADERS[HOUSES[congress].democratic_leader],
			"houseRepLeader" : LEADERS[HOUSES[congress].republican_leader],
			"senateDemLeader" : LEADERS[SENATES[congress].democratic_leader],
			"senateRepLeader" : LEADERS[SENATES[congress].republican_leader]
		}

		data["congressional"].update(
										{ 
											congress : {
													"publicLaws" : enactedLaws,
													"senate" : SENATES[congress],
													"house" : HOUSES[congress],
													"leadership" : leaders
											} 
										}
									)

	# Pass data on number of revisions per title in year.
	data["annual"].update(
							{
								year : {
									"revisions" : YEARS[year]["revisions"],
									"numPublicLaws" : YEARS[year]["numPublicLaws"],
									"titleNames" : YEARS[year]["titleNames"]
								}
							}
						)

	# Identify leadership.
	titleYearlyRevisions = {}
	for ay in ACTIVE_YEARS:
		titleYearlyRevisions[ay] = YEARS[ay]["revisions"][int(title)]
	print titleYearlyRevisions
	data["titular"] = titleYearlyRevisions

	return render_template('year-title-archive.html', year=year, title=title.zfill(2),
							data=data)

@app.route('/archive/annual/<int:year>')
def yearArchiveOverview(year):
	"""Return styled overview of the annual archive."""
	
	data = {
		"annual" : {},
		"congressional" : {}
	}

	# Given year, find relevant Congresses.
	congresses = set()
	for congress, senate in SENATES.iteritems():
		if year >= senate.first_year and year <= senate.last_year:
			congresses.add(senate.ordinality)

	# Given congresses, find all leaders and publicLaws they passed in year.
	for congress in congresses:
		enactedLaws = []
		for publicLawId, publicLaw in PUBLIC_LAWS[congress].iteritems():
			print publicLawId
			if publicLaw.date_enacted.split()[-1] == str(year):
				enactedLaws.append(publicLaw)

		enactedLaws.sort(key = lambda x: datetime.strptime(x.date_enacted, '%B %d, %Y'))

		leaders = {
			"president" : PRESIDENTS[YEARS[year]["president"]],
			"houseDemLeader" : LEADERS[HOUSES[congress].democratic_leader],
			"houseRepLeader" : LEADERS[HOUSES[congress].republican_leader],
			"senateDemLeader" : LEADERS[SENATES[congress].democratic_leader],
			"senateRepLeader" : LEADERS[SENATES[congress].republican_leader]
		}

		data["congressional"].update(
										{ 
											congress : {
													"publicLaws" : enactedLaws,
													"senate" : SENATES[congress],
													"house" : HOUSES[congress],
													"leadership" : leaders
											} 
										}
									)

	# Pass data on number of revisions per title in year.
	data["annual"].update(
							{
								year : {
									"revisions" : YEARS[year]["revisions"],
									"numPublicLaws" : YEARS[year]["numPublicLaws"],
									"titleNames" : YEARS[year]["titleNames"]
								}
							}
						)

	# Compute three most heavily-edited titles, but don't assume we have the data.
	revisions = data["annual"][year]["revisions"]
	titles = revisions.copy()
	if titles.get("total"):
		del titles["total"]
		titles = titles.keys()
		titles.sort(key = lambda x: revisions[x]["ins"] + revisions[x]["del"], reverse=True)
		mostEditedTitles = titles[0:3]
		data["annual"][year].update({"mostEdited" : mostEditedTitles})

	return render_template('year-archive.html', year=year, data=data)

@app.route('/archives/diff/<int:year>/<string:title>')
def annualDiff(year, title):
	"""Return styled annual diff."""
	return render_template('code/diff/%d/usc-%d-%s-diff.html' % (year, year, title))