/*
 *	Reusable Button Navigation
 *
 *			Thu 18 Feb 17:35:50 2016
 */
import React, { Component, PropTypes } from 'react'
import RaisedButton from 'material-ui/lib/raised-button'

class ButtonNav extends Component {
	constructor(props) {
		super(props)
	}

	render() {
		const { back, next } = this.props
		return (
			<div className="row">
				<div className="col-xs-6">
					{ back && 
						<RaisedButton 
							primary={true}
							label="Back"
							onClick={back} 
							/>
					}
				</div>
				<div className="col-xs-6">
					{ next && 
						<RaisedButton 
							secondary={true}
							label="Next"
							onClick={next} 
							/>
					}
				</div>
			</div>
		)
	}	
}

export default ButtonNav
