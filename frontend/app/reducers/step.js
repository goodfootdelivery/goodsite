/*
 *		Step Reducer
 *
 * 					Wed 17 Feb 12:21:40 2016
 *
 */

const initialState = 1

const step = (state=initialState, action) => {
	switch(action.type) {
		case 'NEXT':
			return state + 1

		case 'PREVIOUS':
			return state - 1

		case 'RESET':
			return initialState

		default:
			return state
	}
}

export default step
