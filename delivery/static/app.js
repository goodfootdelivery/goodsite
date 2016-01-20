// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

config = function($interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
};


mainCtrl = function($scope, $resource){
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
AddressCtrl.$inject = [ '$scope', '$resource' ]


// MAIN //
angular
	.module('delivery', ['ngAutocomplete', 'ui.bootstrap', 'ngRoute', 'ngResource'])
	.config(config)
	.controller('mainCtrl', , mainCtrl])
	.factory('addFactory', ['$http', 'addFactory'])
