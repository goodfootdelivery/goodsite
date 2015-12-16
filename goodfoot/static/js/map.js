$(function(){
        
	$("#pickup-geocomplete").geocomplete({
		details: "#start",
		detailsAttribute: "geo",
		types: ["geocode"],
	});

	$("#dropoff-geocomplete").geocomplete({
		details: "#end",
		detailsAttribute: "geo",
		types: ["geocode"],
	});
        
});
