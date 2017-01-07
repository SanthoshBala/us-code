from flask import Flask, render_template
from potus import *
from chamber import *
from congressperson import *

app = Flask(__name__)

##### DATA INITIALIZATION #####

YEARS = {
	1994 : {
		"president" : 42,
		"congress" : 103
	},
	1995 : {
		"president" : 42,
		"congress" : 104
	},
	1996 : {
		"president" : 42,
		"congress" : 104
	},
	1997 : {
		"president" : 42,
		"congress" : 105
	},
	1998 : {
		"president" : 42,
		"congress" : 105
	},
	1999 : {
		"president" : 42,
		"congress" : 106
	},
	2000 : {
		"president" : 42,
		"congress" : 106
	},
	2001 : {
		"president" : 43,
		"congress" : 107
	},
	2002 : {
		"president" : 43,
		"congress" : 107
	},
	2003 : {
		"president" : 43,
		"congress" : 108
	},
	2004 : {
		"president" : 43,
		"congress" : 108
	},
	2005 : {
		"president" : 43,
		"congress" : 109
	},
	2006 : {
		"president" : 43,
		"congress" : 109
	},
	2007 : {
		"president" : 43,
		"congress" : 110
	},
	2008 : {
		"president" : 43,
		"congress" : 110
	},
	2009 : {
		"president" : 44,
		"congress" : 111
	},
	2010 : {
		"president" : 44,
		"congress" : 111
	},
	2011 : {
		"president" : 44,
		"congress" : 112
	},
	2012 : {
		"president" : 44,
		"congress" : 112
	},
	2013 : {
		"president" : 44,
		"congress" : 113
	},
	2014 : {
		"president" : 44,
		"congress" : 113
	},
	2015 : {
		"president" : 44,
		"congress" : 114
	},
	2016 : {
		"president" : 44,
		"congress" : 114
	}
}

PRESIDENTS = {
	42 : POTUS(42, "William", "Clinton", "D", 1993, 2000, "Jefferson", 
					"Bill"),
	43 : POTUS(43, "George", "Bush", "R", 2001, 2008, "Walker"),
	44 : POTUS(44, "Barack", "Obama", "D", 2009, 2016, "Hussein")
}

SENATES = {
	102 : Chamber(102, "Senate", 56, 44, "mitchell", "dole", 
					0, 1991, 1992),
	103 : Chamber(103, "Senate", 57, 43, "mitchell", "dole",
					0, 1993, 1994),
	104 : Chamber(104, "Senate", 48, 52, "daschle", "lott",
					0, 1995, 1996),
	105 : Chamber(105, "Senate", 55, 45, "daschle", "lott",
					0, 1997, 1998),
	106 : Chamber(106, "Senate", 55, 45, "daschle", "lott",
					0, 1999, 2000),
	107 : Chamber(107, "Senate", 50, 49, "daschle", "lott",
					1, 2001, 2002),
	108 : Chamber(108, "Senate", 51, 48, "daschle", "frist",
					1, 2003, 2004),
	109 : Chamber(109, "Senate", 55, 44, "reid", "frist",
					1, 2005, 2006),
	110 : Chamber(110, "Senate", 49, 49, "reid", "mcconnell",
					2, 2007, 2008),
	111 : Chamber(111, "Senate", 57, 41, "reid", "mcconnell",
					2, 2009, 2010),
	112 : Chamber(112, "Senate", 51, 47, "reid", "mcconnell",
					2, 2011, 2012),
	113 : Chamber(113, "Senate", 53, 45, "reid", "mcconnell",
					2, 2013, 2014),
	114 : Chamber(114, "Senate", 44, 54, "reid", "mcconnell",
					2, 2015, 2016)
}

HOUSES = {
	102 : Chamber(102, "House", 267, 167, "foley", "michel", 
					1, 1991, 1992),
	103 : Chamber(103, "House", 258, 176, "foley", "michel",
					1, 1993, 1994),
	104 : Chamber(104, "House", 204, 230, "gephardt", "gingrich",
					1, 1995, 1996),
	105 : Chamber(105, "House", 207, 226, "gephardt", "gingrich",
					2, 1997, 1998),
	106 : Chamber(106, "House", 211, 223, "gephardt", "hastert",
					1, 1999, 2000),
	107 : Chamber(107, "House", 213, 220, "gephardt", "hastert",
					2, 2001, 2002),
	108 : Chamber(108, "House", 205, 229, "pelosi", "hastert",
					1, 2003, 2004),
	109 : Chamber(109, "House", 201, 233, "pelosi", "hastert",
					1, 2005, 2006),
	110 : Chamber(110, "House", 233, 202, "pelosi", "boehner",
					0, 2007, 2008),
	111 : Chamber(111, "House", 257, 178, "pelosi", "boehner",
					0, 2009, 2010),
	112 : Chamber(112, "House", 193, 242, "pelosi", "boehner",
					0, 2011, 2012),
	113 : Chamber(113, "House", 201, 234, "pelosi", "boehner",
					0, 2013, 2014),
	114 : Chamber(114, "House", 188, 247, "pelosi", "ryan",
					0, 2015, 2016)
}

LEADERS = {
	"pelosi" : Congressperson("Nancy", "Pelosi", "House", "D", "CA", 
								1987, middle_name="Patricia D'Alesandro"),
	"boehner" : Congressperson("John", "Boehner", "House", "R", "OH", 
								1991, 2015, "Andrew"),
	"ryan" : Congressperson("Paul", "Ryan", "House", "R", "WI", 
								1999, middle_name="Davis"),
	"gephardt" : Congressperson("Richard", "Gephardt", "House", "D", "MO",
								1977, 2005, "Arnold", "Dick"),
	"michel" : Congressperson("Robert", "Michel", "House", "R", "IL",
								1981, 1995, "Henry", "Bob"),
	"foley" : Congressperson("Thomas", "Foley", "House", "D", "WA",
								1965, 1995, "Stephen", "Tom"),
	"hastert" : Congressperson("John", "Hastert", "House", "R", "IL",
								1987, 2007, "Dennis", "Dennis"),
	"gingrich" : Congressperson("Newton", "Gingrich", "House", "R", "GA",
								1979, 1999, "Leroy", "Newt"),
	"mitchell" : Congressperson("George", "Mitchell", "Senate", "D", "ME",
								1980, 1995, "John"),
	"dole" : Congressperson("Robert", "Dole", "Senate", "R", "KS",
								1969, 1996, "Joseph", "Bob"),
	"lott" : Congressperson("Chester", "Lott", "Senate", "R", "MS",
								1989, 2007, "Trent", "Trent"),
	"daschle" : Congressperson("Thomas", "Daschle", "Senate", "D", "SD",
								1987, 2005, "Andrew", "Tom"),
	"frist" : Congressperson("William", "Frist", "Senate", "R", "TN",
								1995, 2007, "Harrison", "Bill"),
	"reid" : Congressperson("Harry", "Reid", "Senate", "D", "NV",
								1987, 2017, "Mason"),
	"mcconnell" : Congressperson("Addison", "McConnell", "Senate", "R", "KY",
								1985, middle_name="Mitchell", nickname="Mitch")
}

@app.route('/')
def home():
    """Return homepage."""
    return render_template('index.html')

@app.route('/archives/annual/<int:year>/<string:title>')
def annualArchive(year, title):
	"""Return styled annual archive."""
	president = PRESIDENTS[YEARS[year]["president"]]
	senate = SENATES[YEARS[year]["congress"]]
	house = HOUSES[YEARS[year]["congress"]]
	houseDemLeader = LEADERS[house.democratic_leader]
	houseRepLeader = LEADERS[house.republican_leader]
	senateDemLeader = LEADERS[senate.democratic_leader]
	senateRepLeader = LEADERS[senate.republican_leader]

	return render_template('annual-archive.html', year=year, title=title,
							president=president, senate=senate, house=house,
							senateDemLeader=senateDemLeader, 
							senateRepLeader=senateRepLeader,
							houseDemLeader=houseDemLeader,
							houseRepLeader=houseRepLeader)

@app.route('/archives/diff/<int:year>/<string:title>')
def annualDiff(year, title):
	"""Return styled annual diff."""
	return render_template('code/diff/%d/usc-%d-%s-diff.html' % (year, year, title))