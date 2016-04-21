/*
 *			jQuery orderForm Entry point
 *
 *						Sun 13 Mar 13:32:31 2016
 */

import { isLocal, phase, addressIndex, orderMain, setAddr, placeOrder, purchaseOrder } from './ajaxHelpers'
import { datepicker } from 'jquery-ui'
import 'geocomplete'
import 'jquery.cookie'
import './map'

/**
 *	Main jQuery Event Handlers
 */

$(() => {


	/**
	 * Geocomplete & Datepicker Initialization
	 */


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




	/**
	 * Move On To Next Phase Of Order
	 */


	$( '#next' ).click(function(){
		switch (phase){
			case 1:
				$(['start', 'end']).each(function(_, form) {
					setAddr(form)
				})
				break
			case 2:
				placeOrder()
				break
			case 3:
				let chosenRate = $( '#rates input[name=rate]' ).val()
				let obj = { "rate_id": chosenRate }
				purchaseOrder(chosenRate)
				break
			default:
				console.log("PHASE OUT OF BOUNDS")
		}
	});




	/**
	 * Move On To Previous Phase Of Order
	 */


	$( '#back' ).click(function(){});


});
