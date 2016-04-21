/*
 *		AJAX HELPERS FOR GOODFOOT API
 *					Wed  9 Mar 12:39:04 2016
 */

const API_BASE = 'http://localhost:8000/api/'
// const API_BASE = 'http://69c420b0.ngrok.io/api/'

const SML_PARCEL = { "length": 1.00, "width": 1.00, "height": 1.00, "weight": 1.00 }
const MED_PARCEL = { "length": 2.00, "width": 2.00, "height": 2.00, "weight": 2.00 }
const LRG_PARCEL = { "length": 3.00, "width": 3.00, "height": 3.00, "weight": 3.00 }

let orderPK = null
export let addressesLeft = 2
export let phase = 1

export const addressIndex = ['start', 'end']

export let isLocal = true

export const orderMain = {
	pickup: null,
	dropoff: null,
	parcel: SML_PARCEL,
	delivery_date: null,
	ready_time_start: null
}
/*
 *	GOODFOOT API HELPERS
 */

// function callSuccess(data, form){
// 	// Apply Validation & Initiate Next Request
// 	switch (form) {
// 		case "start":
// 			orderMain.pickup = data.id
// 			setAddr('addresses', $( '#end' ).serialize(), 'end')
// 			break;
// 		case "end":
// 			orderMain.dropoff = data.id;
// 			( data.city != "Toronto" )? isLocal = false : isLocal = true
// 			// place order when request are complete
// 			placeOrder()
// 			break;
// 		default:
// 			console.log('Form Name Not Recognized')
// 	}

// 	// Initialize Map
// 	let selector = '#' + form + ' '
// 	let mapURL = $.staticMap({
// 			address: $( selector + ' input[name=geocompleted]' ).val(),
// 			zoom: 18,
// 			height: 200,
// 			width: 300
// 		});
// 	$( selector + ' .address-map' ).attr('src', mapURL)

// 	// Swap Form for Map
// 	$( selector + '.stepOne' ).hide(300)
// 	$( selector + '.stepTwo' ).show(300)
// }


// const buildRates = (rates) => {
// 	// Table Header and Row Initializers
// 	let trHTML = '';
// 	let trHEAD = 'local-rates';
// 	if (!isLocal){
// 		$.each(rates, function (_, rate) {
// 			trHTML += '<tr><td><input type="radio" name="rate" value="' + rate.id + '"></td><td>'
// 				+ rate.carrier + '</td><td>' + '$' + rate.rate + '</td><td>' + rate.service + 
// 				'</td><td>' + rate.days + '</td></tr>';
// 		});
// 		trHEAD = 'non-local-rates'
// 	} else {
// 		$.each(rates, function (_, rate) {
// 			trHTML += '<tr><td><input type="radio" name="rate" value="' + rate.service + '"></td><td>' +
// 				rate.service + '</td><td>' + rate.price + '</td></tr>';
// 		});
// 	}
// 	// Build Table
// 	$( '#' + trHEAD ).show(300)
// 	$('#rates').append(trHTML);
// 	$( '.stepTwo' ).show(300)
// }




/*
 * Geocoder Helper Function
 */


function geoCode(addr) {
	$.ajax({
		url: 'http://geocoder.ca',
		type: 'GET',
		data: {
			locate: addr,
			json: 1
		},
		success: function(response) {
			formattedAddr = '';
			try {
				formattedAddr = {
					street: data.standard.stnumber + ' ' + data.standard.staddress,
					prov: data.standard.prov,
					city: data.standard.city,
					postal: data.postal,
					lat: data.latt,
					lng: data.longt
				}	
			} catch(err) {
				formattedAddr = {}
			} finally {
				return formattedAddr
			}
		},
		error: function(error) {
			console.log(error)
		}
	})
}




/*
 *	Parcel Builder Helper
 */

function getParcel() {
	let size = $( '#details select[name=parcel]' ).val()
	switch (size) {
		case "small":
			return SML_PARCEL
			break;
		case "medium":
			return MED_PARCEL
			break;
		case "large":
			return LRG_PARCEL
			break;
		default:
			return SML_PARCEL
	}	
}




/**
 * Shows and hides sections of Form based on phase variables.
 */


const switchPhase = (phase) => {
	console.log('PHASE SWITCH')
	console.log(phase)
	switch(phase){
		case 1:
			$( '.stepOne' ).show(300)
			$( '.stepTwo' ).hide(300)
			break
		case 2:
			$( '.stepOne' ).hide(300)
			$( '.stepTwo' ).show(300)
			break
		case 3:
			$( '.stepTwo' ).hide(300)
			$( '.stepThree' ).show(300)
			break
		case 4:
			$( '.stepThree' ).hide(300)
			$( '.stepFour' ).show(300)
			break
		default:
			break
	}
}




/*
 *			API CALLS
 *
 *	These Functions make calls to the Goodfoot API
 *
 */




/**
 * Sets a Single Address
 */


export function setAddr(form) {
	let obj = $( '#' + form ).serialize()
	$.ajax({
		url: API_BASE + 'addresses/',
		type: 'POST',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: obj,
		success: function(data) {
			// callSuccess(data, form)
			switch (form){
				case "start":
					orderMain.pickup = data.id
					console.log(orderMain.pickup)
				case "end":
					( data.city != "Toronto" )? isLocal = false : isLocal = true
					orderMain.dropoff = data.id
					console.log(orderMain.dropoff)
				default:
					addressesLeft -= 1
					// Initialize Map
					let selector = '#' + form + ' '
					let mapURL = $.staticMap({
							address: $( selector + ' input[name=geocompleted]' ).val(),
							zoom: 18,
							height: 200,
							width: 300
						});
					$( selector + ' .address-map' ).attr('src', mapURL)
					// console.log("FORM NAME NOT RECOGNIZED")
			}
			if (addressesLeft == 0){
				// $( selector + '.stepOne' ).hide(300)
				// $( selector + '.stepTwo' ).show(300)
				phase +=1
				switchPhase(phase)
			}
		},
		error: function(data) {
			console.log('ADDRESS ERROR')
			let errors = $.parseJSON(data.responseText)
			if ('name' in errors) {
				var selector = "#" + form + " input[name=name]"
				$( selector ).closest('.form-group').addClass('has-error')
			} 
			if ('street' in errors) {
				var addrErr = "#" + form + " input[name=geocompleted]"
				$( addrErr ).closest('.form-group').addClass('has-error')
			}
			if ('postal_code' in errors) {
				var addrErr = "#" + form + " input[name=geocompleted]"
				$( addrErr ).closest('.form-group').addClass('has-error')
			}
		}
	})	
};




/**
 *	Places Order
 */


export function placeOrder() {
	orderMain.parcel = getParcel()
	orderMain.delivery_date = $( '#details input[name=date]' ).val()
	orderMain.ready_time_start = $( '#details select[name=time]' ).val()
	console.log(orderMain)

	$.ajax({
		url: API_BASE + 'orders/',
		type: 'POST',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		contentType: 'application/json',
		data: JSON.stringify(orderMain),
		success: function(response){
			console.log('__ORDER_PLACED__')
			// Set Order ID
			orderPK = response.id
			// Add Rates to Form
			let rates = response.rates
			let trHTML = '';
			let trHEAD = 'local-rates';
			if (!isLocal){
				$.each(rates, function (_, rate) {
					trHTML += '<tr><td><input type="radio" name="rate" value="' + rate.id + '"></td><td>'
						+ rate.carrier + '</td><td>' + '$' + rate.rate + '</td><td>' + rate.service + 
						'</td><td>' + rate.days + '</td></tr>';
				});
				trHEAD = 'non-local-rates'
			} else {
				$.each(rates, function (_, rate) {
					trHTML += '<tr><td><input type="radio" name="rate" value="' + rate.service + '"></td><td>' +
						rate.service + '</td><td>' + rate.price + '</td></tr>';
				});
			}
			// Build Table
			$( '#' + trHEAD ).show(300)
			$('#rates').append(trHTML);
			phase +=1
			switchPhase(phase)
		},
		error: function(error){
			console.log('ORDER CALL ERROR:\n')
			console.log(error.responseText)
			console.log('\n')
			if ('delivery_date' in error.responseJSON) {
				$( '#details input[name=date]' ).closest('.form-group').addClass('has-error')
			}
		}
	})
}




/**
 *	Purchases Order
 */


export function purchaseOrder(rate) {
	$.ajax({
		url: API_BASE + 'orders/' + orderPK + '/',
		type: 'PUT',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		contentType: 'application/json',
		data: JSON.stringify({
			"rate_id": rate
		}),
		success: function(response){
			phase +=1
			switchPhase(phase)
		},
		error: function(error){
			console.log('PURCHASE CALL ERROR:\n')
			console.log(error.responseText)
			console.log('\n')
			console.log(error)
		}
	})
}
