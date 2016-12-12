var YEAR_TITLE_COUNT_MAP = {
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
	2015 : 22
}

function refreshPreIframe() {
    var ifr = document.getElementById("pre-iframe");
    ifr.src = ifr.src;
    ifr.style.height = "";
    ifr.style.height = ifr.contentWindow.document.body.scrollHeight + 'px';
}

function refreshPostIframe() {
    var ifr = document.getElementById("post-iframe");
    ifr.src = ifr.src;
    ifr.style.height = "";
    ifr.style.height = ifr.contentWindow.document.body.scrollHeight + 'px';	
}

function updatePreYearAndOrTitle() {
	var updatedYear = document.getElementById("pre-year-selector").value
	titleSelector = document.getElementById("pre-title-selector")
	var updatedTitle = titleSelector.value
	var ifr = document.getElementById("pre-iframe")
	ifr.src = "../archives/annual/" + updatedYear + "/usc-" + updatedYear + "-" + updatedTitle + ".html"
	ifr.style.height = "";
    ifr.style.height = ifr.contentWindow.document.body.scrollHeight + 'px';

	// Update # of titles that can be chosen
	var newNumTitles = YEAR_TITLE_COUNT_MAP[updatedYear]
	titleSelector.options.length = newNumTitles
	for (var i = 0; i < newNumTitles; i++) {
		titleSelector.options[i] = new Option(i + 1, i + 1)
	}
}