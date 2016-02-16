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
	getInitialState: function(){
		return {
			formatted: '',
			// Geocode Results
			address: {
				street: '',
				postal: '',
				prov: '',
				city: '',
				latt: '',
				longt: ''
			}
		}
	},

	onChange: function(e){
		this.setState({formatted: e.target.value});
	},
	
	setAddress: function(){
		var _this = this;

		$.ajax({
			url: 'http://geocoder.ca/',
			data: {
				locate: _this.state.formatted,
				json: 1
			},
			datatype: 'json',
			cache: false,
			success: function(data){
				_this.setState({
					address: {
						street: data.standard.stnumber + ' ' + data.standard.staddress,
						prov: data.standard.prov,
						city: data.standard.city,
						postal: data.postal,
						latt: data.latt,
						longt: data.longt
					}
				})
			}
		})
	},

	render: function(){
		return(
				<div className="row">
					<div className="col-xs-12">
						<TextField
								hintText='ex: 720 Bathurst St, Toronto ON'
								floatingLabelText='Pickup Address'
								onChange={this.onChange}
								value={this.state.formatted}
								onBlur={this.setAddress}
								/>
					</div>
				</div>
			  )
	}
 })

export default GeoCode
