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
import CircularProgress from 'material-ui/lib/circular-progress'
// Container Classes
import Start from './start'
import AddressPair from './addressPair.js'
import Details from './details.js'
/*
 * Allow Tap Event with Material UI
 */
import injectTapEventPlugin from 'react-tap-event-plugin'
injectTapEventPlugin()

/*
 *	Main Form Switcher
 */
const DeliveryApp = ({step, isFetching}) => (
	<div>
		{ step == 1 && <Start /> }
		{ step == 2 && <AddressPair /> }
		{ step == 3 && <Details /> }

			<br></br>
			
		{ isFetching && <CircularProgress /> }
	</div>
)

/*
 *	Container Component
 */
const mapStateToProps = (state) => {
	return {
		step: state.process.step,
		isFetching: state.process.isFetching
	}
}

export default connect(mapStateToProps)(DeliveryApp)
