/*
 *		Is Fetching Error Handler
 *
 *				Thu 18 Feb 15:28:33 2016
 *
 */
const initialState = false

const isFetching = (state=initialState, action) => {
	switch(action.type) {
		case 'FETCHING':
			return true
		case 'SET_ADDRESSES':
			return false
		default:
			return state
	}
}

export default isFetching
