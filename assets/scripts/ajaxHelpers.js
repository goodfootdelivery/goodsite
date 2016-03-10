/*
 *		AJAX HELPERS FOR GOODFOOT API
 *					Wed  9 Mar 12:39:04 2016
 */

var API_BASE = 'http://localhost:8000/api/'

var isLocal = true

var orderMain = {
	pickup: null,
	dropoff: null,
	parcel: {
		"length": 1.00,
		"width": 1.00,
		"height": 1.00,
		"weight": 1.00
	}
}

/*
 * GEOCODE HELPER
 */

// takes a string
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
 *	GOODFOOT API HELPERS
 */

function callSuccess(data, form){
	console.log(data)
	if (form === 'start') {
		orderMain.pickup = data.id
	} else if (form === 'end') {
		orderMain.dropoff = data.id;
		( data.city != "Toronto" )? isLocal = false : isLocal = true
	}
	console.log(orderMain)
}

function callError(data, form){
	if ('name' in data) {
		var selector = "#" + form + " input[name=name]"
		$( selector ).closest('.form-group').addClass('has-error')
	} 

	var addrErr = "#" + form + " input[name=geocompleted]"
	$( addrErr ).closest('.form-group').addClass('has-error')

	console.log(data)
}

// Throws an Object Error
function callAPI(url, obj, form) {
	$.ajax({
		url: API_BASE + url +'/',
		type: 'POST',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: obj,
		success: function(data) {
			callSuccess(data, form)
		},
		error: function(data) {
			callError(data.responseJSON, form)
		}
	})	
};

function placeOrder(data, isLocal) {
	$.ajax({
		url: API_BASE + 'orders/',
		type: 'POST',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: data,
		success: function(response){
			var trHTML = '';
			if (isLocal){
				$.each(response, function (_, rate) {
					trHTML += '<tr><td><input type="radio" name=rate value="' + rate.id + '"></td><td>'
						+ rate.carrier + '</td><td>' + '$' + rate.rate + '</td><td>' + rate.service + 
						'</td><td>' + rate.days + '</td></tr>';
				});
			} else {
				$.each(response, function (_, rate) {
					trHTML += '<tr><td><input type="radio" name=rate value="' + rate.service + '"></td><td>'
						+ rate.price + '</td></tr>';
				});
			}
			// Build Table
			$( '#rates-head' ).show(300)
			$('#rates').append(trHTML);
		},
		error: function(error){
			throw error
		}
	})
}

function purchase(pk, rate) {
	$.ajax({
		url: API_BASE + 'orders/' + pk + '/',
		type: 'PUT',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: rate,
		success: function(response){
			return response
		},
		error: function(error){
			console.log(error)
		}
	})
}
