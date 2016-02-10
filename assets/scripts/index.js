var React = require('react')
var ReactDOM = require('react-dom')

var Address = React.createClass({
	 render: function(){
		 return(
					<fieldset className="form-group">
						<label className="control-label" for="address">Address</label>
						<input 
							name="address"
							placeholder="ex: 720 Bathurst St, Toronto, ON"
							className="form-control"
							type="text"
						/>
					</fieldset>



			   )
		   
	 }
 })

ReactDOM.render(<Address />, document.getElementById('order'))
