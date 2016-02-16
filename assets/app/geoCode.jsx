/*
 *
 *			ADDRESS React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 */

import React from 'react';
import TextField from 'material-ui/lib/text-field';

/*
 * ADDRESS
 */
var GeoCode = React.createClass({
	getInitialState: function(){
		return {
			address: '',
			// Geocode Results
			street: '',
			postal: '',
			prov: '',
			city: '',
			latt: '',
			longt: ''
		}
	},

	onChange: function(e){
		this.setState({address: e.target.value});
	},
	
	setAddress: function(){
		var _this = this;

		$.ajax({
			url: 'http://geocoder.ca/',
			data: {
				locate: _this.state.address,
				json: 1
			},
			datatype: 'json',
			cache: false,
			success: function(data){
				_this.props.saveValues({
					street: data.standard.stnumber + ' ' + data.standard.staddress,
					prov: data.standard.prov,
					city: data.standard.city,
					postal: data.postal,
					latt: data.latt,
					longt: data.longt
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
								value={this.state.address}
								onBlur={this.setAddress}
								/>
						<ul>
							<li>Street: {this.state.street}</li>
							<li>Province: {this.state.prov}</li>
							<li>City: {this.state.city}</li>
							<li>Latitude: {this.state.latt}</li>
							<li>{this.state.longt}</li>
						</ul>
					</div>
				</div>
			  )
	}
 })

module.exports = GeoCode;
