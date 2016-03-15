/*
 *		Detail REACT Components
 *
 *				Tue 16 Feb 23:39:07 2016
 *
 */

import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import { reset, setAddresses } from '../actions.js';
// Material-UI
import DatePicker from 'material-ui/lib/date-picker/date-picker';
import TimePicker from 'material-ui/lib/time-picker/time-picker';
import RaisedButton from 'material-ui/lib/raised-button'
import TextField from 'material-ui/lib/text-field'
import RadioButtonGroup from 'material-ui/lib/radio-button-group';
import RadioButton from 'material-ui/lib/radio-button';
import ButtonNav from '../components/buttonNav.js'

const styles = {
	block: {
		maxWidth: 250,
	},
	radioButton: {
		marginBottom: 16,
	},
};


/*
 *	Default Parcel Sizes
 */
const smParcel = { length: 1.2, width: 2.3, height: 3.4, weight: 4.5 }
const mdParcel = { length: 1.2, width: 2.3, height: 7.4, weight: 4.5 }
const lgParcel = { length: 4.2, width: 5.3, height: 3.4, weight: 4.5 }

/*
 *	Nested Detail Component
 */
class Details extends Component {
	constructor(props) {
		super(props)
		this.build = this.build.bind(this)
	}

	build() {
		let data = {}
		// Get Parcel
		if(this.props.isLocal) {
			switch(this.refs.parcel.getValue()) {
				case 'SMALL':
					data.parcel = smParcel
				case 'MEDIUM':
					data.parcel = mdParcel
				case 'LARGE':
					data.parcel = lgParcel
			}
		} else {
			data.parcel.length = this.refs.length.getValue()
			data.parcel.width = this.refs.width.getValue()
			data.parcel.height = this.refs.height.getValue()
			data.parcel.weight = this.refs.height.getValue()
		}
		// Get Date & TIME
		data.date = this.refs.date.getValue()
		data.time = this.refs.time.getValue()
		// Pass to Prop Function
		this.props.placeOrder(data)
	}

	render() {
		return (
			<div>
				<div className="row">
					<h3>Date, Time & Parcel</h3>
				</div>

				<br></br>
				
				<div className='row'>
					{ this.props.isLocal?
						<div className="col-xs-6">
							<RadioButtonGroup ref='parcel' defaultSelected='SMALL' name="Parcel" style={styles.block}>
								<RadioButton
									value='SMALL'
									label="Small (max 1 x 2 x 3 x 4lb)"
									style={styles.radioButton}
									/>
								<RadioButton
									value='MEDIUM'
									label="Medium (max 4 x 5 x 6 x 7lb)"
									style={styles.radioButton}
									/>
								<RadioButton
									value='LARGE'
									label="Large (max 8 x 9 x 11 x 50lb)"
									style={styles.radioButton}
									/>
							</RadioButtonGroup>	
						</div>
					:
						<div>
							<div className="col-xs-2">
								<TextField 
									ref='length'
									fullWidth={true}
									floatingLabelText='Length (in)'
									/>
							</div>
							<div className="col-xs-2">
								<TextField 
									ref='height'
									fullWidth={true}
									floatingLabelText='Height (in)'
									/>
							</div>
							<div className="col-xs-2">
								<TextField 
									ref='width'
									fullWidth={true}
									floatingLabelText='Width (in)'
									/>
							</div>
							<div className="col-xs-2">
								<TextField 
									ref='weight'
									fullWidth={true}
									floatingLabelText='Weight (lb)'
									/>
							</div>
						</div>
					}	
					<div className="col-xs-3">
						<DatePicker
							ref='date'
							hintText='Pickup Date'	
							mode="landscape"
							/>
					</div>
					<div className="col-xs-3">
						<TimePicker
							ref='time'
							hintText='Pickup Time'	
							format="ampm"
							/>
					</div>
				</div>

				<br></br>
				
				<ButtonNav 
					back={this.props.reset} 
					next={this.props.next(
						{
							"pickup": this.props.pickup,
							"dropoff": this.props.dropoff
						}	
					)}
					/>
			</div>
		)
	}
}


/*
 *	Detail Container Section
 */
const mapStateToProps = (state) => {
	return {
		isLocal: state.order.isLocal,
		pickup: state.order.pickup
	}	
}
const mapDispatchToProps = (dispatch) => {
	return {
		reset: () => {
			dispatch(reset())
		},
		next: (data) => {
			dispatch(setAddresses(data))
		},
		placeOrder: (data) => {
			dispatch(place(data))
		}
	}
}

// Detail Container Component
export default connect(mapStateToProps, mapDispatchToProps)(Details)
