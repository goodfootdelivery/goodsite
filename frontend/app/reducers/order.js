/*
 *		ORDER Reducer
 *
 * 					Wed 17 Feb 12:21:40 2016
 *
 */

const initialState = {
	isLocal: true	
}


const order = (state=initialState, action) => {
	switch(action.type) {
		case 'SET_ADDRESSES':
			console.log(action.data)
			return Object.assign({}, state, action.data)

		case 'RESET':
			return initialState

		case 'NEXT':
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
