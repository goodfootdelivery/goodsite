/*
 *		STARTING GEOCODER COMPONENT
 *
 *					Mon 15 Feb 18:19:43 2016
 *
 */

import React, { PropTypes, Component } from 'react';
import { connect } from 'react-redux';
// My Components
import { setAddresses } from '../actions.js';
import GeoCode from './geoCode.js';
import RaisedButton from 'material-ui/lib/raised-button';


/*
 *	Nested Component
 */
const Start = React.createClass({
	setAddr: function(){
		this.props.onSubmit({
			pickup: this.refs.pickup.state.address,
			dropoff: this.refs.dropoff.state.address
		})
	},

	render: function() {
		return (
			<div>
				<div className="row">
					<div className="col-xs-6">
						<GeoCode 
							label='Pickup Address'
							ref='pickup' 
							/>
					</div>
					<div className="col-xs-6">
						<GeoCode 
							label='Dropoff Address'
							ref='dropoff' 
							/>
					</div>
				</div>

				<br></br>
				
				<div className="row">
					<div className="col-xs-6"> </div>
					<div className="col-xs-6">
						<RaisedButton 
							secondary={true}
							label='Next'
							onClick={this.setAddr} 
							/>
					</div>
				</div>
			</div>
		);
	}
})


/*
 *	Container Section
 */
const mapStateToProps = (state) => {
	return {}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		onSubmit: (data) => {
			dispatch(setAddresses(data))
		}
	}
}
// Container Component
const StartContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Start)

export default StartContainer
