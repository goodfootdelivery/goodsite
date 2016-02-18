/*
 *		ORDER FLUX APPLICATION ENTRY
 *
 *					Tue 16 Feb 17:01:46 2016
 */

import React, { PropTypes } from 'react'
import { render } from 'react-dom'
import { createStore, combineReducers, applyMiddleware } from 'redux'
import thunk from 'redux-thunk'
import { Provider } from 'react-redux'
// Reducers
import step from './reducers/step'
import order from './reducers/order'
import isFetching from './reducers/isFetching'
// Containers
import DeliveryApp from './containers/deliveryApp'


/*
 *	Reducer Dispatcher
 */
const store = createStore(
	combineReducers({ 
		step, 
		order,
		isFetching
	}),
	applyMiddleware(thunk)
)


/*
 *	Root Render Function
 */
render(
	<Provider store={store}>
		<DeliveryApp />
	</Provider>,
	document.getElementById('order')
)
