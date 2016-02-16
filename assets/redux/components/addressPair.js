/*
 *
 *			ADDRESS PAIR React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 *			i/	Determines if order is Local
 *
 */

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import Address from './address.js'
import FlatButton from 'material-ui/lib/flat-button'

/*
 * AddressPair
 */
const AddressPair = React.createClass({
	next: function() {
		this.props.nextStep()
	},

	render: function() {
		return (
				<div>
					<div className="row">
						<div className="col-xs-6">
							<Address ref='pickup' address={this.props.pickup} />
						</div>
						<div className="col-xs-6">
							<Address ref='dropoff' address={this.props.dropoff}/>
						</div>
					</div>
					<div className="row">
						<div className="col-xs-6">
						</div>
						<div className="col-xs-6">
							<FlatButton 
								label="next"
								onClick={this.submit} 
								/>
						</div>
					</div>
				</div>
		)
	}
})

const mapStateToProps = (state) => {
	return {
		pickup: state.order.pickup,
		dropoff: state.order.dropoff
	}	
}

const AddressCon = connect(
	mapStateToProps
)(AddressPair)

export default AddressCon
