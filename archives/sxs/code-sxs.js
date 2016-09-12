function refreshPreIframe() {
    var ifr = document.getElementById("pre-iframe");
    ifr.src = ifr.src;
}

function refreshPostIframe() {
    var ifr = document.getElementById("post-iframe");
    ifr.src = ifr.src;
}

function updatePreYearAndOrTitle() {
	var updatedYear = document.getElementById("pre-year-selector").value
	var updatedTitle = document.getElementById("pre-title-selector").value
	var ifr = document.getElementById("pre-iframe")
	ifr.src = "../annual/" + updatedYear + "/usc-" + updatedYear + "-" + updatedTitle + ".html"
	
}