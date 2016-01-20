// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

var config = function($interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
};


var addressServ = function($resource){
	var url = 'http://jsonplaceholder.typicode.com/users/:user';
	return $resource(url, {user: '@user'})
};
addressServ.$inject = ['$resource'];


mainCtrl = function($scope, $resource, $http, addressServ){
	$scope.pickup = {},
	$scope.dropoff = {},

	$scope.options = {
		country: 'ca',
		types: 'geocode',
	};

	$scope.users = addressServ.query();

	// var user_data = $http.get('http://jsonplaceholder.typicode.com/users');
	// user_data.then( function(result){
	// 		$scope.users = result.data;
	// } );

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
mainCtrl.$inject = [ '$scope', '$resource', '$http', 'addressServ' ]

// MAIN //
angular
	.module('delivery', [
		'ngAutocomplete',
		'ui.bootstrap',
		'ngRoute',
		'ngResource'
	])

	.config(config)
	.controller('mainCtrl', mainCtrl)
	.factory('addressServ', addressServ)
