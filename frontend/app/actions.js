/*
 *			ACTIONS
 *
 *					Tue 16 Feb 17:00:14 2016
 */

import axios from 'axios'
import Cookies from 'js-cookie'

const API_BASE = 'http://localhost:8000/api'
const GEO_BASE = 'http://geocoder.ca'

const NEXT = 'NEXT'
const PREVIOUS = 'PREVIOUS'
const FETCHING = 'FETCHING'

const SET_ADDRESSES = 'SET_ADDRESSES'
const CHECK_ADDRESSES = 'CHECK_ADDRESSES'

const SET_PICKUP = 'SET_PICKUP'
const SET_DROPOFF = 'SET_DROPOFF'
const FIX_PICKUP = 'FIX_PICKUP'
const FIX_DROPOFF = 'FIX_DROPOFF'

const RESET = 'RESET'
const PLACE = 'PLACE'

/*
 *	API Axios Instance
 */
const API = axios.create({
	baseURL: API_BASE,
	timeout: 1000,
	headers: {'X-CSRFToken': Cookies.get('csrftoken')}
})

/*
 *	Geocoding Axios Instance
 */
const GEO = axios.create({
	timeout: 1000
})


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
	} catch(err) {
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
export const nextStep = () => {
	return {
		type: NEXT,
	}
}

export const previousStep = () => {
	return {
		type: PREVIOUS
	}
}


export const fetch = () => {
	return {
		type: FETCHING
	}	
}

export const setAddresses = (data) => {
	let url = '/addresses/'
	return (dispatch) => {
		dispatch(fetch())
		// Try Pickup
		API.post('/addresses/', data)
			.then( (response) => {
				dispatch({ type: SET_PICKUP, data: response })
			})
			.catch( (response) => {
				dispatch({ type: FIX_PICKUP, data: response })
			})
		// Try Dropoff
		API.post('/addresses/', data)
			.then( (response) => {
				dispatch({ type: SET_DROPOFF, data: response })
			})
			.catch( (response) => {
				dispatch({ type: FIX_DROPOFF, data: response })
			})
	}
}

export const geoCodeAddresses = (data) => {
	return (dispatch) => {
		//Fetching Indicator
		dispatch(fetch())
		// Build Addresses
		return axios.all([
			GEO.get(GEO_BASE, { params: { locate: data.pickup, json: 1 } }),
			GEO.get(GEO_BASE, { params: { locate: data.dropoff, json: 1 } })
		])
			.then(axios.spread(
				(pickupResponse, dropoffResponse) => {
					let addrData = {
						pickup: geoSet(pickupResponse.data),
						dropoff: geoSet(dropoffResponse.data)
					}
					// End Debugging
					dispatch({ type: 'SET_ADDRESSES', data: addrData })	
					dispatch(nextStep())
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
