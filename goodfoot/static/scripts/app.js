// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

config = function($routeProvider, $interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
	$routeProvider
		.when('/delivery', {
			templateUrl: '/static/views/orderForm.html',
			controller: 'mainCtrl',
			controllerAs: 'vm'
		})
		.when('/account', {
			templateUrl: '/static/views/account.html',
			controller: 'accountCtrl',
			controllerAs: 'am'
		})
		.otherwise({
			redirectTo: '/delivery'
		});
};

orderServ = function($resource){
	var url = 'http://127.0.0.1:8000/api/addresses/';
	// var url = 'http://jsonplaceholder.typicode.com/users/:user';
	return $resource(url)
};


// MAIN //
angular
	.module('delivery', [
		'ngAutocomplete',
		'ui.bootstrap',
		'angular.google.distance',
		// 'djangoRESTResources',
		'uiGmapgoogle-maps',
		'ngRoute',
		'ngResource'
	])

	.config(config)
	.controller('mainCtrl', mainCtrl)
	.controller('accountCtrl', accountCtrl)
	.controller('confirmCtrl', confirmCtrl)
	.directive('addressForm', addressForm)
	.directive('dateForm', dateForm)
	.directive('parcelForm', parcelForm)
	.factory('orderServ', orderServ)
