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
class Address extends Component {
	constructor(props) {
		super(props)
		this.build = this.build.bind(this)
	}

	build() {
		return {
			street: this.refs.street.getValue(),
			unit: this.refs.unit.getValue(),
			city: this.refs.city.getValue(),
			prov: this.refs.prov.getValue(),
			postal: this.refs.postal.getValue(),
			name: this.refs.name.getValue(),
			phone: this.refs.phone.getValue()
		}	
	}

	render() {
		return (
				<div>
					<div className="row">
						<div className="col-xs-8">
							<TextField 
								ref='street'
								fullWidth={true}
								defaultValue={this.props.address.street}
								floatingLabelText='Street'
									/>
						</div>
						<div className="col-xs-4">
							<TextField 
								ref='unit'
								fullWidth={true}
								defaultValue={this.props.address.unit}
								floatingLabelText='Apt.'
									/>
						</div>
					</div>
					<div className="row">
						<div className="col-xs-5">
							<TextField 
								ref='city'
								fullWidth={true}
								defaultValue={this.props.address.city}
								floatingLabelText='City'
									/>
						</div>
						<div className="col-xs-2">
							<TextField 
								ref='prov'
								fullWidth={true}
								defaultValue={this.props.address.prov}
								floatingLabelText='Prov.'
									/>
						</div>
						<div className="col-xs-5">
							<TextField 
								ref='postal'
								fullWidth={true}
								defaultValue={this.props.address.postal}
								floatingLabelText='Postal Code'
									/>
						</div>
					</div>
					<div className="row">
						<div className="col-xs-7">
							<TextField 
								ref='name'
								fullWidth={true}
								defaultValue={this.props.address.name}
								floatingLabelText='Name/Company'
									/>
						</div>
						<div className="col-xs-5">
							<TextField 
								ref='phone'
								fullWidth={true}
								defaultValue={this.props.address.phone}
								floatingLabelText='Phone'
									/>
						</div>
					</div>
				</div>
		)
	}
}

export default Address
