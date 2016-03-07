/*
 *		ORDER Reducer
 *
 * 					Wed 17 Feb 12:21:40 2016
 *
 */

const initialState = {
	isLocal: true,
	pickup: {
		country: 'CA'
	},
	dropoff: {
		country: 'CA'
	}
}


const order = (state=initialState, action) => {
	switch(action.type) {
		case 'SET_ADDRESSES':
			return Object.assign({}, state, action.data)

		case 'RESET':
			return initialState

		case 'CHECK_ADDRESSES':
			(state.dropoff.city.toUpperCase() !== 'TORONTO')?
				action.data.isLocal = false 
			: 
				action.data.isLocal = true	
			return Object.assign({}, state, action.data)

		default:
			return state
	}
}

export default order
