/*
 *		STARTING GEOCODER COMPONENT
 *
 *					Mon 15 Feb 18:19:43 2016
 *
 */

import React, { PropTypes, Component } from 'react';
import { connect } from 'react-redux';
// My Components
import { geoCodeAddresses } from '../actions.js';
import Address from '../components/address.js';
import ButtonNav from '../components/buttonNav.js'

import DatePicker from 'react-datepicker'
import moment from 'moment'
require('react-datepicker/dist/react-datepicker.css');

import TimePicker from 'material-ui/lib/time-picker/time-picker'
import SelectField from 'material-ui/lib/select-field'
import MenuItem from 'material-ui/lib/menus/menu-item'
import TextField from 'material-ui/lib/text-field'



/*
 *	Nested Component
 */
class StartOrder extends Component {
	constructor(props) {
		super(props)
		this.next = this.next.bind(this)
	}

	next() {
		this.props.onSubmit({
			pickup: this.refs.pickup.getValue(),
			dropoff: this.refs.dropoff.getValue()
		})
	}

	render() {
		return (
			<div>
				<div className="row">
					<div className="col-xs-6">
						<legend>Pickup</legend>
						<Address 
							address={this.props.pickup}
							label='Pickup Address'
							ref='pickup' 
							/>
						<legend>Date & Time</legend>
						<div className="row">
							<div className="col-xs-7">
								<DatePicker 
									ref='date'
									/>
							</div>
							<div className="col-xs-5">
								<TimePicker
									ref='time'
									hintText='Pickup Time'	
									format="ampm"
									/>
							</div>
						</div>
						<div className="row">
							<div className="col-xs-12">
								<TextField
									hintText="Additional Information Here i.e Buzzer"
									multiLine={true}
									rows={2}
									rowsMax={4}
									/>
							</div>
						</div>
					</div>
					<div className="col-xs-6">
						<legend>Dropoff</legend>
						<Address 
							address={this.props.dropoff}
							label='Dropoff Address'
							ref='dropoff' 
							/>
						<div className="row">
							<SelectField value={1} >
								<MenuItem value={1} primaryText="Small"/>
								<MenuItem value={2} primaryText="Medium"/>
								<MenuItem value={3} primaryText="Large"/>
							</SelectField>
						</div>
						<div className="row">
							<ButtonNav/>
						</div>
					</div>
				</div>

			</div>
		)
	}
}


/*
 *	Container Section
 */
const mapStateToProps = (state) => {
	console.log(state)
	return {
		pickup: state.order.pickup.address,
		dropoff: state.order.dropoff.address
	}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		onSubmit: (data) => {
			dispatch(geoCodeAddresses(data))
		}
	}
}
// Container Loader
export default connect(mapStateToProps, mapDispatchToProps)(StartOrder)
