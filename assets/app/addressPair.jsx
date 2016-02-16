/*
 *
 *			ADDRESS PAIR React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 *			i/	Determines if order is Local
 *
 */

import React from 'react';
import Address from './address.jsx';
import GeoCode from './geoCode.jsx'
import DateTime from './dateTime.jsx';
import FlatButton from 'material-ui/lib/flat-button'

/*
 * AddressPair
 */
var AddressPair = React.createClass({
	next() {
		this.props.nextStep()
	},

	render() {
		return(
				<div className="row">
					<div className="col-xs-6">
						// PICKUP
						{ jQuery.isEmptyObject(this.props.pickup)
							? <GeoCode saveValues={this.props.saveValues}/>
							: <Address 
								address={this.props.pickup}
								/> }

						
					</div>
					<div className="col-xs-6">
						// DROPOFF
						{ jQuery.isEmptyObject(this.props.dropoff)
							? <GeoCode saveValues={this.props.saveValues}/>
							: <Address 
								address={this.props.dropoff}
								/> }
					</div>
					<div className="col-xs-12">
						<FlatButton
							label='Next'
							onClick={this.next}
							/>
					</div>
				</div>
				);
	}
})

module.exports = AddressPair
