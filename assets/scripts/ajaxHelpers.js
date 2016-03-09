/*
 *		AJAX HELPERS FOR GOODFOOT API
 *					Wed  9 Mar 12:39:04 2016
 */

var API_BASE = 'http://localhost:8000/api/'

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
	console.log(data + form)
}

function callError(data, form){
	if ('name' in data) {
		var selector = "#" + form + " input[name=name]"
		$( selector ).closest('.form-group').addClass('has-error')
	} 

	var addrErr = "#" + form + " input[name=geocompleted]"
	$( addrErr ).closest('.form-group').addClass('has-error')
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
			callSuccess(data.responseJSON, form)
		},
		error: function(data) {
			callError(data.responseJSON, form)
		}
	})	
};

function getRates(pk) {
	$.ajax({
		url: API_BASE + 'orders/' + pk + '/rates/',
		type: 'GET',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		success: function(response){
			return response
		},
		error: function(error){
			throw error
		}
	})
}

function purchase(pk, rate) {
	$.ajax({
		url: API_BASE + 'orders/' + pk + '/rates/',
		type: 'POST',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: rate,
		success: function(response){
			return response
		},
		error: function(error){
			throw error
		}
	})
}
