import injectTapEventPlugin from 'react-tap-event-plugin';
import React from 'react';
import ReactDOM from 'react-dom';
import TextField from 'material-ui/lib/text-field';

// Allow Tap Event with Material UI
injectTapEventPlugin();

var Address = React.createClass({
	getInitialState: function(){
		return {
			address: '',
			// Geocode Results
			staddress: '',
			stnumber: '',
			postal: '',
			prov: '',
			city: '',
			latt: '',
			longt: ''
		}
	},

	onChange: function(e){
		this.setState({address: e.target.value});
	},
	
	setAddress: function() {
		var _this = this;

		$.ajax({
			url: 'http://geocoder.ca/',
			data: {
				locate: _this.state.address,
				json: 1
			},
			datatype: 'json',
			cache: false,
			success: function(data){
				_this.setState({
					staddress: data.standard.staddress,
					stnumber: data.standard.stnumber,
					prov: data.standard.prov,
					city: data.standard.city,
					postal: data.postal,
					latt: data.latt,
					longt: data.longt
				})
			}
		})
	},

	render: function(){
		return(
				<div className="row">
					<div className="col-xs-6">
						<TextField
							hintText='ex: 720 Bathurst St, Toronto ON'
							floatingLabelText='Pickup Address'
							onChange={this.onChange}
							value={this.state.address}
							onBlur={this.setAddress}
						/>
					</div>
					<div className="col-xs-6">
						<TextField
							hintText='ex: 17 Raglan Ave, Toronto ON'
							floatingLabelText='Dropoff Address'
						/>
					</div>
					<div className="col-xs-12">
						<ul>
							<li>{this.state.stnumber}</li>
							<li>{this.state.staddress}</li>
							<li>{this.state.prov}</li>
							<li>{this.state.city}</li>
							<li>{this.state.latt}</li>
							<li>{this.state.longt}</li>
						</ul>
					</div>
				</div>
			  )
	}
 })

ReactDOM.render(<Address />, document.getElementById('order'))
