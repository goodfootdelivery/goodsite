/*
 *		AJAX HELPERS FOR GOODFOOT API
 *					Wed  9 Mar 12:39:04 2016
 */

const API_BASE = 'http://localhost:8000/api/'

const SML_PARCEL = { "length": 1.00, "width": 1.00, "height": 1.00, "weight": 1.00 }
const MED_PARCEL = { "length": 2.00, "width": 2.00, "height": 2.00, "weight": 2.00 }
const LRG_PARCEL = { "length": 3.00, "width": 3.00, "height": 3.00, "weight": 3.00 }

let orderPK = null

export let isLocal = true

export const orderMain = {
	pickup: null,
	dropoff: null,
	parcel: SML_PARCEL,
	delivery_date: null,
	delivery_time: null
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
	switch (form) {
		case "start":
			orderMain.pickup = data.id
			break;
		case "end":
			orderMain.dropoff = data.id;
			( data.city != "Toronto" )? isLocal = false : isLocal = true
			break;
		default:
			console.log('Form Name Not Recognized')
	}
}

function callError(data, form){
	if ('name' in data) {
		var selector = "#" + form + " input[name=name]"
		$( selector ).closest('.form-group').addClass('has-error')
	} 
	if ('street' in data) {
		var addrErr = "#" + form + " input[name=geocompleted]"
		$( addrErr ).closest('.form-group').addClass('has-error')
	}
	if ('postal_code' in data) {
		var addrErr = "#" + form + " input[name=geocompleted]"
		$( addrErr ).closest('.form-group').addClass('has-error')
	}

	console.log(data)
}

// Throws an Object Error
export function callAPI(url, obj, form) {
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

export function placeOrder() {
	orderMain.parcel = getParcel()
	orderMain.delivery_date = $( '#details input[name=date]' ).val()
	orderMain.delivery_time = $( '#details select[name=time]' ).val()
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
			// Set Order ID
			orderPK = response.order.id
			let rates = response.rates
			// Table Header and Row Initializers
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
			$( '#stepOne' ).hide(300)
			$( '#stepTwo' ).show(300)
		},
		error: function(error){
			if ('delivery_date' in error.responseJSON) {
				$( '#details input[name=date]' ).closest('.form-group').addClass('has-error')
			}
		}
	})
}

export function purchaseOrder(rate) {
	console.log(rate)
	$.ajax({
		url: API_BASE + 'orders/' + orderPK + '/',
		type: 'PUT',
		headers: {
			'X-CSRFToken': $.cookie( 'csrftoken' )
		},
		data: { "rate_id": rate },
		success: function(response){
			$( '#stepTwo' ).hide(300)
			$( '#stepThree' ).show(300)
		},
		error: function(error){
			console.log(error)
		}
	})
}
