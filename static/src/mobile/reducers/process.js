/*
 *		Process Reducer
 *
 *				Thu 18 Feb 15:28:33 2016
 *
 */

import { combineReducers } from 'redux'

const step = (state=1, action) => {
	switch(action.type) {
		case 'NEXT':
			return state + 1

		case 'PREVIOUS':
			return state - 1

		case 'RESET':
			return 1

		default:
			return state
	}
}

const isFetching = (state=false, action) => {
	switch(action.type) {
		case 'FETCHING':
			return true

		case 'NEXT':
			return false

		case 'PREVIOUS':
			return false

		default:
			return state
	}
}

export default process = combineReducers({
	step,
	isFetching
})
