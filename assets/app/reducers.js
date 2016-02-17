/*
 *		Main Reducer 
 *				Mon 15 Feb 11:47:21 2016
 */
import react from 'react';
import { combineReducers } from 'redux';

const initialState = {
	step: 1,
	isLocal: false,
	order: {}
}

const orderApp = (state=initialState, action) => {
	switch(action.type) {
		case 'SET_ADDRESSES':
			var newState = {
				step: state.step + 1,
				order: action.data
			}
			return Object.assign({}, state, newState)
		case 'RESET':
			return initialState
		case 'NEXT':
			var newState = {
				step: state.step + 1,
				order: action.data
			}
			return Object.assign({}, state, newState)

		default:
			return state
	}
};

export default orderApp
