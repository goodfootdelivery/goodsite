/**
 * Account Controller for Whole
 *
 *				Mon Feb  1 12:24:32 2016
 *
 * @ngInject
 */

accountCtrl = function(){
	var self = this;

	self.oneAtATime = true;
	self.status = {
		isFirstOpen: true,
		isFirstDisabled: false
	};
	
	self.orders = [
		{
			title: '#78415',
			pickup: '17 Raglan Ave',
			dropoff: '720 Bathurst St',
			service: 'Express',
			parcel: {
				length: 13.23,
				height: 57.65,
				width: 14.32,
				weight: 87.21,
			},
			price: '$17.50'
		},
		{
			title: '#54767',
			pickup: '143 Something Street',
			dropoff: '87 Nowhere Ave',
			service: 'Same Day',
			parcel: {
				length: 13.23,
				height: 57.65,
				width: 14.32,
				weight: 87.21,
			},
			price: '$98.21'
		}
	];
		
};
