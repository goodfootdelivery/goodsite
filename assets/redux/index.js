/*
 *			ORDER FORM ENTRY POINT
 *
 *
 */
import React, { PropTypes } from 'react'
import { render } from 'react-dom'
import { Provider } from 'react-redux'
import { createStore } from 'redux'

import OrderCon from './components/order.js'
import orderApp from './reducers.js'


let store = createStore(orderApp)

render(
	<Provider store={store}>
		<OrderCon />
	</Provider>,
	document.getElementById('order')
)
