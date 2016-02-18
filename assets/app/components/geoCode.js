/*
 *
 *			GEOCODE React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 */

import React from 'react';
import TextField from 'material-ui/lib/text-field';

/*
 * GEOCODE
 */


var GeoCode = React.createClass({
	getValue: function(){
		return this.refs.address.getValue()
	},

	render: function(){
		return(
				<div className="row">
					<div className="col-xs-12">
						<TextField
								ref='address'
								hintText='ex: 720 Bathurst St, Toronto ON'
								floatingLabelText={this.props.label}
								/>
					</div>
				</div>
			  )
	}
 })

export default GeoCode
