/*
 *			ACTIONS
 *
 *					Tue 16 Feb 17:00:14 2016
 */

import axios from 'axios'

const NEXT = 'NEXT'
const SET_ADDRESSES = 'SET_ADDRESSES'
const RESET = 'RESET'
const PLACE = 'PLACE'


/*
 *	Helper Functions
 */
const geoSet = (data) => {
	let formattedAddr
	try {
		formattedAddr = {
			street: data.standard.stnumber + ' ' + data.standard.staddress,
			prov: data.standard.prov,
			city: data.standard.city,
			postal: data.postal,
			latt: data.latt,
			longt: data.longt
		}	
	} catch(err){
		formattedAddr = {}
	} finally {
		return formattedAddr
	}
}

const listCookies = () => {
    var theCookies = document.cookie.split(';');
    var aString = '';
    for (var i = 1 ; i <= theCookies.length; i++) {
        aString += i + ' ' + theCookies[i-1] + "\n";
    }
    return aString;
}


/*
 *	Action Creators
 */
export const nextStep = (data) => {
	console.log(listCookies())
	return {
		type: NEXT,
		data
	}
}

export const fetch = () => {
	return {
		type: 'FETCHING'
	}	
}

export const tester = (data) => {
	let url = 'http://localhost:8000/api/addresses/'
	return (dispatch) => {
		axios.post(
			url,
			data
		)
			.then((response) => {
				console.log(response)
			})
			.catch((response) => {
				console.log(response.data)
			})
	}
}

export const setAddresses = (data) => {
	let url = 'http://geocoder.ca'
	return (dispatch) => {
		//Fetching Indicator
		dispatch(fetch())
		// Build Addresses
		return axios.all([
			axios.get(url, { params: { locate: data.pickup, json: 1 } }),
			axios.get(url, { params: { locate: data.dropoff, json: 1 } })
		])
			.then(axios.spread(
				(pickupResponse, dropoffResponse) => {
					let addrData = {
						pickup: geoSet(pickupResponse.data),
						dropoff: geoSet(dropoffResponse.data)
					}
					// End Debugging
					dispatch({ 
						type: 'SET_ADDRESSES',
						data: addrData
					})	
				}
			))
	}
}

export const reset = () => {
	return {
		type: RESET
	}
}

export const place = (data) => {
	return {
		type: PLACE,
		data
	}
}
