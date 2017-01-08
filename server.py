from flask import Flask, render_template
from database import *

app = Flask(__name__)



@app.route('/')
def home():
    """Return homepage."""
    return render_template('index.html')

@app.route('/archive/annual/<int:year>/<string:title>')
def yearTitleArchive(year, title):
	"""Return styled annual archive."""
	
	# Summarize congressional year.
	senate = SENATES[YEARS[year]["congress"]]
	house = HOUSES[YEARS[year]["congress"]]
	publicLaws = [ value for key, value in PUBLIC_LAWS[senate.ordinality].iteritems() if value.date_enacted.split()[-1] == str(year)]

	# Identify leadership.
	president = PRESIDENTS[YEARS[year]["president"]]
	houseDemLeader = LEADERS[house.democratic_leader]
	houseRepLeader = LEADERS[house.republican_leader]
	senateDemLeader = LEADERS[senate.democratic_leader]
	senateRepLeader = LEADERS[senate.republican_leader]
	

	numTitles = YEARS[year]["numTitles"]
	
	yearlyRevisions = YEARS[year]["revisions"]

	titleInsertions = YEARS[year]["revisions"][int(title)]["ins"]
	titleDeletions = YEARS[year]["revisions"][int(title)]["del"]

	return render_template('year-title-archive.html', year=year, title=title.zfill(2),
							president=president, senate=senate, house=house,
							senateDemLeader=senateDemLeader, 
							senateRepLeader=senateRepLeader,
							houseDemLeader=houseDemLeader,
							houseRepLeader=houseRepLeader,
							numTitles=numTitles, titleInsertions=titleInsertions,
							titleDeletions=titleDeletions,
							publicLaws=publicLaws)

@app.route('/archives/diff/<int:year>/<string:title>')
def annualDiff(year, title):
	"""Return styled annual diff."""
	return render_template('code/diff/%d/usc-%d-%s-diff.html' % (year, year, title))