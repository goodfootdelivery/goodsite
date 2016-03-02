/*
 *
 *			ADDRESS PAIR React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 *			i/	Determines if order is Local
 *
 */

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { reset, checkAddresses } from '../actions.js';
import Address from '../components/address.js'
import RaisedButton from 'material-ui/lib/raised-button'


/*
 * Nested Component
 */
class AddressPair extends Component {
	constructor(props) {
		super(props)
		this.set = this.set.bind(this)
	}

	set() {
		let data = {
			pickup: this.refs.pickup.build(),
			dropoff: this.refs.dropoff.build()
		}
		this.props.next(data)
	}

	render() {
		return (
				<div>
					<div className="row">
						<div className="col-xs-6">
							<h2>Pickup</h2>
							<Address ref='pickup' address={this.props.pickup} />
						</div>
						<div className="col-xs-6">
							<h2>Dropoff</h2>
							<Address ref='dropoff' address={this.props.dropoff}/>
						</div>
					</div>

					<br></br>
					
					<div className="row">
						<div className="col-xs-6">
							<RaisedButton 
								primary={true}
								label="Back"
								onClick={this.props.reset} 
								/>
						</div>
						<div className="col-xs-6">
							<RaisedButton 
								secondary={true}
								label="Next"
								onClick={this.set} 
								/>
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
	console.log(state.order)
	return {
		pickup: state.order.pickup,
		dropoff: state.order.dropoff
	}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		next: (data) => {
			dispatch(checkAddresses(data))
		},
		reset: () => {
			dispatch(reset())
		}
	}
}

// Container Component
export default connect(mapStateToProps, mapDispatchToProps)(AddressPair)
