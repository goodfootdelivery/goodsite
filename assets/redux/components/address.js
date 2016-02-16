/*
 *
 * 			Address React Component
 *
 */

import React, { PropTypes, Component } from 'react';
import TextField from 'material-ui/lib/text-field';

/*
 * Address Form
 */
const Address = React.createClass({
	render: function() {
		return (
				<div>
					<div className="row">
						<div className="col-xs-8">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.street}
								floatingLabelText='street'
									/>
						</div>
						<div className="col-xs-4">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.unit}
								floatingLabelText='unit'
									/>
						</div>
					</div>
					<div className="row">
						<div className="col-xs-5">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.city}
								floatingLabelText='city'
									/>
						</div>
						<div className="col-xs-2">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.prov}
								floatingLabelText='prov'
									/>
						</div>
						<div className="col-xs-5">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.postal}
								floatingLabelText='postal'
									/>
						</div>
					</div>
					<div className="row">
						<div className="col-xs-7">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.name}
								floatingLabelText='name'
									/>
						</div>
						<div className="col-xs-5">
							<TextField 
								fullWidth={true}
								defaultValue={this.props.address.phone}
								floatingLabelText='number'
									/>
						</div>
					</div>
				</div>
		)
	}
})

export default Address
