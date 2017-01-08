function updateYear() {
	var updatedYear = document.getElementById("year-selector").value;
	
	var currentUrl = window.location.href;
	var urlElements = currentUrl.split("/");
	urlElements[urlElements.length - 2] = updatedYear;
	var newUrl = urlElements.join("/");

	window.location.href = newUrl;

	return false;
}

function updateTitle() {
	var updatedTitle = document.getElementById("title-selector").value;

	var currentUrl = window.location.href;
	var urlElements = currentUrl.split("/");
	urlElements[urlElements.length - 1] = updatedTitle;
	var newUrl = urlElements.join("/");

	window.location.href = newUrl;

	return false;
}

function injectDiffCounts() {
	var numInsertions = document.getElementsByTagName("ins").length;
	var numDeletions = document.getElementsByTagName("del").length;

	insertionSpan = document.getElementById("num-insertions");
	deletionSpan = document.getElementById("num-deletions");

	insertionSpan.textContent = numInsertions;
	deletionSpan.textContent = numDeletions;
}