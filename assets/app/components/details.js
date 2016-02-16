import React, { Component, PropTypes } from 'react'
import { connect } from 'react-redux'
import DatePicker from 'material-ui/lib/date-picker/date-picker';
import TimePicker from 'material-ui/lib/time-picker/time-picker';

const Details = React.createClass({
	render: function(){
		return (
			<div>
				<div class="col-xs-3">
					<DatePicker
							mode="landscape"
							/>
				</div>
				<div class="col-xs-3">
					<TimePicker
							format="ampm"
							/>
				</div>
				<div class="col-xs-6"></div>
			</div>
		)
	}
})

const mapStateToProps = (state) => {
	return {
		isLocal: state.isLocal,
	}
}

export default DetailContainer
