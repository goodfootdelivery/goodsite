/*
 *		ORDER Reducer
 *
 * 					Wed 17 Feb 12:21:40 2016
 *
 */

import { combineReducers } from 'redux'

/*
 *	Initial States
 */
const initialAddressState = {
	address: {
		country: 'CA'
	},
	errors: {}
}

const initialOrderState = {
	isLocal: true,
	order: {
		pickup: null,
		dropoff: null,
		parcel: {},
		service: 'BA',
		date: new Date(),
		time: new Date(),
		comments: null
	},
	errors: {}
}

/*
 *	Reducers
 */
const pickupReducer = (state=initialAddressState, action) => {
	switch(action.type) {
		case 'SET_ADDRESSES':
			const obj = Object.assign({}, state.address, action.data)
			console.log('order.js')
			console.log(obj)
			return obj

		case 'RESET':
			return initialAddressState

		case 'FIX_PICKUP':
			return state
		default:
			return state
	}
}

const dropoffReducer = (state=initialAddressState, action) => {
	switch(action.type) {
		case 'SET_DROPOFF':
			return Object.assign({}, state.address, action.data)

		case 'RESET':
			return initialAddressState

		case 'CHECK_ADDRESSES':
			(state.address.city.toUpperCase() !== 'TORONTO')?
				action.data.isLocal = false 
			: 
				action.data.isLocal = true	
			return Object.assign({}, state, action.data)
		case 'FIX_DROPOFF':
			return state
		default:
			return state
	}
}

const orderReducer = (state=initialOrderState, action) => {
	switch(action.type) {
		case 'SET_DROPOFF':
			return Object.assign({}, state, action.data)

		case 'RESET':
			return initialOrderState

		case 'CHECK_ADDRESSES':
			(state.dropoff.city.toUpperCase() !== 'TORONTO')?
				action.data.isLocal = false 
			: 
				action.data.isLocal = true	
			return Object.assign({}, state, action.data)
		case 'FIX_DROPOFF':
			return state
		default:
			return state
	}
}

/*
 *	Aggregate Reducer
 *
 */
const order = combineReducers({
	pickup: pickupReducer,
	dropoff: dropoffReducer,
	order: orderReducer	
})

export default order
