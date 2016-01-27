TestCtrl = function(GoogleDistanceAPI){
	var self = this;
	self.options = {
		country: 'ca',
		types: 'geocode',
	};

	self.help = function(){
		if (self.pickup && self.dropoff){
			console.log('aye');
			var args = {
				origins: [self.pickup.result],
				destinations: [self.dropoff.result]
			};
			GoogleDistanceAPI
				.getDistanceMatrix(args)
				.then(function(data){
					self.distance = data.rows[0].elements[0].distance.value;
					// console.log(self.distance)
				});
		} else {
			console.log('nay')
		};
	};
	self.help();
};
TestCtrl.$inject = ['GoogleDistanceAPI'];

