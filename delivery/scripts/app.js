// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

config = function($interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
};

// addressServ = function($resource){
// 	var url = 'http://127.0.0.1:8000/api/addresses/';
// 	// var url = 'http://jsonplaceholder.typicode.com/users/:user';
// 	return $resource(url, {user: '@user'})
// };


// MAIN //
angular
	.module('delivery', [
		'ngAutocomplete',
		'ui.bootstrap',
		'angular.google.distance',
		'ngResource'
	])

	.config(config)
	.controller('TestCtrl', TestCtrl)
	// .controller('mainCtrl', mainCtrl)
	// .controller('DateController', DateController)
	// .controller('PickupController', PickupController)
	// .factory('addressServ', addressServ)
