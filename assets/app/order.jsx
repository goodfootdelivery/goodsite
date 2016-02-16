/*
 *
 *			ORDER FORM React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 *
 *		i/	Components implements stage changes in the order process.
 *
 */

import React from 'react';
import ReactDOM from 'react-dom';
// My Components
import Address from './address.jsx';
import AddressPair from './addressPair.jsx';
import DateTime from './dateTime.jsx';
/*
 * Allow Tap Event with Material UI
 */
import injectTapEventPlugin from 'react-tap-event-plugin';
injectTapEventPlugin();


/*
 * Complete Field Data Set
 */
var fieldValues = {
	pickup: {},
	dropoff: {},
	parcel: {},
	date: null,
	service: null,
};

/*
 * If The Order Is Local
 */
var isLocal = true;


/*
 *Top Level Dispatcher
 */
var OrderForm = React.createClass({
	getInitialState: function(){
		return {
			step: 1
		}
	},

	nextStep: function(){
		this.setState({
			step: this.state.step + 1
		})
	},

	previousStep: function(){
		this.setState({
			step: this.state.step - 1
		})
	},
	
	/*
	* Update Field Data
	*/
	saveValues: function(fields) {
		return function() {
			fieldValues = Object.assign({}, fieldValues, fields)
		}()
	},

	render: function(){
		switch(this.state.step){
			case 1:
				return <AddressPair 
							pickup = { fieldValues.pickup }
							dropoff = { fieldValues.dropoff }
							isLocal = { isLocal }
							saveValues = { this.saveValues }
							nextStep = { this.nextStep }
							/>

			case 2:
				return <Address address={ fieldValues.pickup }/>
		}
	}
});

ReactDOM.render(<OrderForm />, document.getElementById('order'))
