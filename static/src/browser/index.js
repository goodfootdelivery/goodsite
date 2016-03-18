/*
 *			jQuery orderForm Entry point
 *
 *						Sun 13 Mar 13:32:31 2016
 */

import { isLocal, orderMain, callAPI, placeOrder, purchaseOrder } from './ajaxHelpers'
import { datepicker } from 'jquery-ui'
import 'geocomplete'
import 'jquery.cookie'
import './map'

/**
 *	Main jQuery Event Handlers
 */

$(() => {

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
		dateFormat: "yy-mm-dd",
		changeMonth: true,
		changeYear: false,
		minDate: new Date(),
		beforeShowDay: $.datepicker.noWeekends
	});

	$( '#next' ).click(function(){
		// Address Building
		callAPI('addresses', $( '#start' ).serialize(), 'start')
		callAPI('addresses', $( '#end' ).serialize(), 'end')
		placeOrder()


		// Map Stuff
		var pickup_url = $.staticMap({
				address: $( '#start input[name=geocompleted]' ).val(),
				zoom: 18,
				height: 200,
				width: 300
			}); $( '#pickup-map' ).attr('src', pickup_url)

		var dropoff_url = $.staticMap({
				address: $( '#end input[name=geocompleted]' ).val(),
				zoom: 16,
				height: 200,
				width: 300
			}); $( '#dropoff-map' ).attr('src', dropoff_url)

	})

	$( '#submit' ).click(function(){
		let chosenRate = $( '#rates input[name=rate]' ).val()
		purchaseOrder(chosenRate)
	})

// document.ready() end..
});
