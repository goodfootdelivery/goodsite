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
import { reset, setAddresses } from '../actions.js';
import Address from '../components/address.js'
import ButtonNav from '../components/buttonNav.js'
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
		this.props.next({
			pickup: this.refs.pickup.build(),
			dropoff: this.refs.dropoff.build()
		})
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
					
					<ButtonNav
						back={this.props.reset}
						next={this.set}
						/>
				</div>
		)
	}
}


/*
 *	Container Section
 */
const mapStateToProps = (state) => {
	console.log('addressPair.js')
	console.log(state)
	return {
		pickup: state.order.pickup.address,
		dropoff: state.order.dropoff.address
	}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		next: (data) => {
			dispatch(setAddresses(data))
		},
		reset: () => {
			dispatch(reset())
		}
	}
}

// Container Component
export default connect(mapStateToProps, mapDispatchToProps)(AddressPair)
