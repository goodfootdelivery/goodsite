/*
 *			ADDRESS ACTIONS
 *
 *					Thu  3 Mar 13:30:55 2016
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


export const setAddr = (data, success, error) => {
	API.post('/addresses/', data)
		.then( (response) => {
			return {
				type: success,
				data
			}
		})
		.catch( (response) => {
			return {
				type: error,
				data
			}
		})
}
