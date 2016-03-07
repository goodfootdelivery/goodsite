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
import GeoCode from '../components/geoCode.js';
import ButtonNav from '../components/buttonNav.js'
import RaisedButton from 'material-ui/lib/raised-button';


/*
 *	Nested Component
 */
class Start extends Component {
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
						<GeoCode 
							label='Pickup Address'
							ref='pickup' 
							/>
					</div>
					<div className="col-xs-6">
						<GeoCode 
							label='Dropoff Address'
							ref='dropoff' 
							/>
					</div>
				</div>

				<br></br>
				
				<ButtonNav next={this.next} />

			</div>
		);
	}
}


/*
 *	Container Section
 */
const mapStateToProps = (state) => {
	return {}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		onSubmit: (data) => {
			dispatch(geoCodeAddresses(data))
		}
	}
}
// Container Loader
export default connect(mapStateToProps, mapDispatchToProps)(Start)
