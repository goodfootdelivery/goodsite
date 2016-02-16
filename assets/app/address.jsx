/*
 *
 * 			Address React Component
 *
 */

import React from 'react';
import TextField from 'material-ui/lib/text-field';

/*
 * Address Form
 */
var Address = React.createClass({

	render: function(){
		return (
				<div>
					// Street & Unit
					<div className="row">
						<div className="col-sm-8">
							<TextField 
								defaultValue={this.props.address.street}
								floatingLabelText='street'
									/>
						</div>
						<div className="col-sm-4"></div>
							<TextField 
								defaultValue={this.props.address.unit}
								floatingLabelText='unit'
									/>
					</div>
					// City & Postal Code
					<div className="row">
						<div className="col-sm-5">
							<TextField 
								defaultValue={this.props.address.city}
								floatingLabelText='city'
									/>
						</div>
						<div className="col-sm-2">
							<TextField 
								defaultValue={this.props.address.city}
								floatingLabelText='prov'
									/>
						</div>
						<div className="col-sm-5"></div>
							<TextField 
								defaultValue={this.props.address.postal}
								floatingLabelText='postal'
									/>
					</div>
					// Name
					<div className="row">
						<div className="col-sm-7">
							<TextField 
								defaultValue={this.props.address.name}
								floatingLabelText='city'
									/>
						</div>
						<div className="col-sm-5"></div>
							<TextField 
								defaultValue={this.props.address.phone}
								floatingLabelText='city'
									/>
					</div>
				</div>
			   )	
	}
})

module.exports = Address
