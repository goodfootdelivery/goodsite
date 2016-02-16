/*
 *
 *			Date & Time React Component
 *
 *						Thu 11 Feb 15:07:31 2016
 *
 */

import React from 'react';
import DatePicker from 'material-ui/lib/date-picker/date-picker';
import TimePicker from 'material-ui/lib/time-picker/time-picker';
/*
 * Date
 */
var DateTime = React.createClass({



	render: function(){
		return(
				<div>
					<DatePicker
							mode="landscape"
							/>
					<TimePicker
							format="ampm"
							/>
				</div>
			  )	
	}
});

module.exports = DateTime
