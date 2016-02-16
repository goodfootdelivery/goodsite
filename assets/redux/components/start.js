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
import FlatButton from 'material-ui/lib/flat-button';

const Start = React.createClass({
	setAddr: function(){
		this.props.dispatch(
			setAddresses({
				pickup: this.refs.pickup.state.address,
				dropoff: this.refs.dropoff.state.address
			})
		)

	},
	render: function() {
		return (
			<div>
				<div className="row">
					<div className="col-xs-6">
						<GeoCode ref='pickup' />
					</div>
					<div className="col-xs-6">
						<GeoCode ref='dropoff' />
					</div>
				</div>
				<div className="row">
					<div className="col-xs-6"></div>
					<div className="col-xs-6">
						<FlatButton 
							label='Next'
							onClick={this.setAddr} 
							/>
					</div>
				</div>
			</div>
		);
	}
})

const StartContainer = connect()(Start)

export default StartContainer
