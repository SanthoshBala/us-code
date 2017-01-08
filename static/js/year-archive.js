function updateYear() {
	var updatedYear = document.getElementById("year-selector").value;
	
	var currentUrl = window.location.href;
	var urlElements = currentUrl.split("/");
	urlElements[urlElements.length - 1] = updatedYear;
	var newUrl = urlElements.join("/");

	window.location.href = newUrl;

	return false;
}