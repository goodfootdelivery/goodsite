/*
 *			ACTIONS
 *
 *					Mon 15 Feb 11:46:24 2016
 */

const NEXT = 'NEXT'
const SET_ADDRESSES = 'SET_ADDRESSES'
const RESET = 'RESET'


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
