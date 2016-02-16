/*
 *			ACTIONS
 *
 *					Tue 16 Feb 17:00:14 2016
 */

const NEXT = 'NEXT'
const SET_ADDRESSES = 'SET_ADDRESSES'
const RESET = 'RESET'

/*
 *	Action Creators
 */
export const nextStep = (data) => {
	return {
		type: NEXT,
		data
	}
}

export const setAddresses = (data) => {
	return {
		type: SET_ADDRESSES,
		data
	}
}

export const reset = () => {
	return {
		type: RESET
	}
}
