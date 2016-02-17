import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import DatePicker from 'material-ui/lib/date-picker/date-picker';
import TimePicker from 'material-ui/lib/time-picker/time-picker';
import TextField from 'material-ui/lib/text-field'
import RadioButtonGroup from 'material-ui/lib/radio-button-group';
import RadioButton from 'material-ui/lib/radio-button';

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
const smParcel = 'small'
const mdParcel = 'medium'
const lgParcel = 'large'

/*
 *	Nested Detail Component
 */
const Details = React.createClass({
	render: function(){
		return (
			<div>
				<div className="row">
					<h3>Date, Time & Parcel</h3>
				</div>

				<br></br>
				
				<div className='row'>
					{ this.props.isLocal?
						<div className="col-xs-6">
							<RadioButtonGroup defaultSelected={ smParcel } name="Parcel" style={styles.block}>
								<RadioButton
									value={ smParcel }
									label="Small (max 1 x 2 x 3 x 4lb)"
									style={styles.radioButton}
									/>
								<RadioButton
									value={ mdParcel }
									label="Medium (max 4 x 5 x 6 x 7lb)"
									style={styles.radioButton}
									/>
								<RadioButton
									value={ lgParcel }
									label="Small (max 8 x 9 x 11 x 50lb)"
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
							hintText='Pickup Date'	
							mode="landscape"
							/>
					</div>
					<div className="col-xs-3">
						<TimePicker
							hintText='Pickup Time'	
							format="ampm"
							/>
					</div>
				</div>
			</div>
		)
	}
})


/*
 *	Detail Container Section
 */
const mapStateToProps = (state) => {
	return {
		isLocal: state.isLocal
	}	
}
const mapDispatchToProps = (dispatch) => {
	return {}
}

// Detail Container Component
const DetailsContainer = connect(
	mapStateToProps,
	mapDispatchToProps
)(Details)

export default DetailsContainer
