function scrollToNextDiff() {
	var insTags = document.getElementsByTagName("ins");
	var delTags = document.getElementsByTagName("del");
	
	for (i = 0; i < insTags.length; i++) {
		relativeHeight = insTags[i].getBoundingClientRect()["top"];
		if (relativeHeight > 161) {
			window.scrollBy(0, relativeHeight - 160);
			break;
		} else {
			continue;
		}
	}
}

function scrollToPreviousDiff() {
	var insTags = document.getElementsByTagName("ins");
	var delTags = document.getElementsByTagName("del");
	
	for (i = insTags.length - 1; i >= 0; i--) {
		relativeHeight = insTags[i].getBoundingClientRect()["top"];
		if (relativeHeight < 160) {
			window.scrollBy(0, relativeHeight - 160);
			break;
		} else {
			continue;
		}
	}
}