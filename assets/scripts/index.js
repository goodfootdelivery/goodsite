var React = require('react')
var ReactDOM = require('react-dom')

var Address = React.createClass({
	getInitialState: function(){
		return {
			address: '',
			// Geocode Results
			staddress: '',
			stnumber: '',
			prov: '',
			city: '',
			latt: '',
			longt: ''
		}
	},
	
	onChange: function(e){
		this.setState({address: e.target.value});
		var self = this;

		$.ajax({
			type: "POST",
			url: 'http://geocoder.ca/',
			data: {
				// auth: "346996985342841253579x3007",
				// locate: self.state.address,
				locate: '720 Bathurst St, Toronto, ON',
				json: 1
			},
			datatype: 'json',
			cache: false,
			success: function(data){
				self.setState({
					staddress: data.match.staddress,
					stnumber: data.match.stnumber,
					prov: data.match.prov,
					city: data.match.city,
					latt: data.latt,
					longt: data.longt
				})
			}
		})
	},

	render: function(){
		return(
				<div>
					<fieldset className="form-group">
					<label className="control-label" htmlFor="address">Address</label>
					<input 
						name="address"
						type="text"
						placeholder="ex: 720 Bathurst St, Toronto, ON"
						className="form-control"
						value={this.state.address}
						onChange={this.onChange}
						/>
					</fieldset>
					<ul>
					<li>{this.state.stnumber}</li>
					<li>{this.state.staddress}</li>
					<li>{this.state.prov}</li>
					<li>{this.state.city}</li>
					<li>{this.state.latt}</li>
					<li>{this.state.longt}</li>
					</ul>
				</div>
			  )
	}
 })

ReactDOM.render(<Address />, document.getElementById('order'))
