$(document).ready(function(){
	// Order JSON OBJECT

	$( "#start input[name=geocompleted]" ).geocomplete({
		details: "#start",
		detailsAttribute: "geo",
		types: ["geocode"],
	});

	$( "#end input[name=geocompleted]" ).geocomplete({
		details: "#end",
		detailsAttribute: "geo",
		types: ["geocode"],
	});

	$( '#date' ).datepicker({
		defaultDate: new Date(),
		changeMonth: true,
		changeYear: false,
		minDate: new Date(),
		beforeShowDay: $.datepicker.noWeekends
	});

	$( '#next' ).click(function(){
		// Address Building
		callAPI('addresses', $( '#start' ).serialize(), 'start')
		callAPI('addresses', $( '#end' ).serialize(), 'end')


		// Map Stuff
		var pickup_url = $.staticMap({
				address: $( '#start input[name=geocompleted]' ).val(),
				zoom: 18,
				height: 200,
				width: 300
			})
		var dropoff_url = $.staticMap({
				address: $( '#end input[name=geocompleted]' ).val(),
				zoom: 16,
				height: 200,
				width: 300
			})
		$( '#pickup-map' ).attr('src', pickup_url)
		$( '#dropoff-map' ).attr('src', dropoff_url)

		// API ADDRESS TEST CALL


		// $( '#stepOne' ).hide(300)
		$( '#stepTwo' ).show(300)

	})
})
