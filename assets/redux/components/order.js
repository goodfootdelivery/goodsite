/*
 *
 *			ORDER FORM React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 *
 *		i/	Components implements stage changes in the order process.
 *
 */

import React, { PropTypes } from 'react'
import { connect } from 'react-redux'

import AddressContainer from './addressPair.js'
import GeoCode from './geoCode.js';
import StartContainer from './start'
/*
 * Allow Tap Event with Material UI
 */
import injectTapEventPlugin from 'react-tap-event-plugin'
injectTapEventPlugin()

/*
 *	Main Form Switcher
 */
const Order = ({step}) => (
	<div>
		{ step == 1 && <StartContainer /> }
		{ step == 2 && <AddressContainer /> }
	</div>
)
/*
 *	Restrictions for Props
 */
Order.PropTypes = {
	step: PropTypes.number
}


/*
 *	Containertainer Component
 */
const mapStateToProps = (state) => {
	return {
		step: state.step
	}
}

const OrderContainer = connect(
	mapStateToProps
)(Order)

export default OrderContainer;
