// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

Config = function($interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
};

AddressCtrl = function($scope){
	$scope.options = {
		country: 'ca',
		types: 'geocode',
	};

	$scope.check = function(){
		if($scope.pickup.details){
			$scope.form = {};
			$scope.form['street'] = $scope.pickup.details.name;
			$scope.form['city'] = $scope.pickup.details.address_components[4].short_name;
			$scope.form['region'] = $scope.pickup.details.address_components[6].short_name;
			$scope.form['country'] = $scope.pickup.details.address_components[7].short_name;
			$scope.form['postal_code'] = $scope.pickup.details.address_components[8].short_name;
			$scope.form['lat'] = $scope.pickup.details.geometry.location.lat();
			$scope.form['lng'] = $scope.pickup.details.geometry.location.lng();
		};
		$scope.pickup.reference = 'HERE';
	};
};

addFactory = function($http){
	var url = '127.0.0.1:8000/delivery/check/';
};

// MAIN //
angular
	.module('delivery', ['ngAutocomplete', 'ui.bootstrap', 'ngAnimate'])
	.config(Config)
	.controller('AddressCtrl', ['$scope', AddressCtrl])
	.factory('addFactory', ['$http', 'addFactory'])
