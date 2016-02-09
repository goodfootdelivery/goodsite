/**
 * Main Controller for Whole
 * Order Process
 * @ngInject
 */
mainCtrl = function($uibModal, GoogleDistanceAPI, orderServ, $http){
	var self = this;
	self.service = 'SD';

	// self.dropoff = {};
	// self.pickup = {};

	// Google Autocomplete Restrictions
	self.options = {
		country: 'ca',
		types: ['address'],
	};

	var call = function(){
		$http.post('http://127.0.0.1:8000/api/addresses/', self.pickup)
			.then(function successCallback(response) {
				self.plink = response.data.link;
			}, function errorCallback(response) { });
		$http.post('http://127.0.0.1:8000/api/addresses/', self.dropoff)
			.then(function successCallback(response) {
				self.dlink = response.data.link;
			}, function errorCallback(response) { });

		if(self.plink && self.dlink){
			self.order = {
				pickup: self.plink,
				dropoff: self.dlink,
				parcel: self.parcel,
				order_date: self.date,
				service: self.service
			};
		};
	};

	self.placeOrder = function(){
		$http.post('http://127.0.0.1:8000/api/orders/', self.order)
			.then(function successCallback(response) {
				self.big = response.data.link;
			}, function errorCallback(response) {
				self.big = response;
			});
	};

	self.getRates = function(){
		$http.get(self.big + 'rates/')
			.then(function successCallback(response) {
				self.rates = response;
			}, function errorCallback(response) { });
	};


	self.orders = orderServ.get();

	var getDistance = function(pickup, dropoff){
		if (pickup && dropoff){
			var args = {
				origins: [pickup],
				destinations: [dropoff]
			};
			GoogleDistanceAPI
				.getDistanceMatrix(args)
				.then(function(data){
					self.distance = data.rows[0].elements[0].distance.value;
					getPrices(self.distance);
				});
		}
	};

	var getPrices = function(value){
		var calc = (fac, min, max) => {
			price = value*fac
			if (min > price) { return min }
			else if (max < price) { return max }
			else { return price };
		};
		self.prices = {
			'basic': calc(0.04, 8.50, 50).toFixed(2),
			'express': calc(0.12, 15, 75).toFixed(2)
		};
	};

	var addressBuild = function(address){
		if(address.details){
			address['street'] = address.details.name;
			address['city'] = address.details.address_components[4].short_name;
			address['region'] = address.details.address_components[6].short_name;
			address['country'] = address.details.address_components[7].short_name;
			address['postal_code'] = address.details.address_components[8].short_name;
			address['lat'] = address.details.geometry.location.lat();
			address['lng'] = address.details.geometry.location.lng();
		};
	};
	

	self.check = function(){
		if(self.pickup && self.dropoff){
			getDistance(self.pickup.result, self.dropoff.result);
			addressBuild(self.pickup);
			addressBuild(self.dropoff);
			call(self.pickup.form);
		}
	};


	self.open = function (size) {
		var modalInstance = $uibModal.open({
			animation: true,
			templateUrl: '/static/views/confirm.html',
			resolve: {
				pmap: {
					center: {latitude: self.pickup.lat, longitude: self.pickup.lng},
					zoom: 16
				},
				dmap: {
					center: {latitude: self.dropoff.lat, longitude: self.dropoff.lng},
					zoom: 16
				},
			},
			controller: 'confirmCtrl as mm',
			size: size,
		});
	};

};
// mainCtrl.$inject = ['$uibModal', 'GoogleDistanceAPI', 'orderServ'];
