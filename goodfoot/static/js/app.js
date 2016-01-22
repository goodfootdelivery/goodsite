// GoodFoot Delivery Order Application
// Thu 14 Jan 17:29:49 2016

config = function($interpolateProvider){
	$interpolateProvider.startSymbol('||').endSymbol('||')
};

// addressServ = function($resource){
// 	// var url = 'http://127.0.0.1:8000/api/addresses/'
// 	var url = 'http://jsonplaceholder.typicode.com/users/:user';
// 	return $resource(url, {user: '@user'})
// };
// mainCtrl.$inject = ['$resource'];

mainCtrl = function($scope){
	$scope.lrg = {"length":3.2, "width":3.2, "height":3.2, "weight":3.2};
	$scope.sml = {"length":1.2, "width":1.2, "height":1.2, "weight":1.2};
	$scope.med = {"length":2.2, "width":2.2, "height":2.2, "weight":2.2};

	$scope.arrowkeys = false;
	$scope.time = new Date();
	$scope.today = function() {
		$scope.dt = new Date();
	};
	$scope.today();

	$scope.clear = function() {
	$scope.dt = null;
	};

	// Disable weekend selection
	$scope.disabled = function(date, mode) {
	return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
	};

	$scope.toggleMin = function() {
	$scope.minDate = $scope.minDate ? null : new Date();
	};

	$scope.toggleMin();
	$scope.maxDate = new Date(2020, 5, 22);

	$scope.open1 = function() {
	$scope.popup1.opened = true;
	};

	$scope.open2 = function() {
	$scope.popup2.opened = true;
	};

	$scope.setDate = function(year, month, day) {
	$scope.dt = new Date(year, month, day);
	};

	$scope.dateOptions = {
	formatYear: 'yy',
	startingDay: 1
	};

	$scope.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
	$scope.format = $scope.formats[0];
	$scope.altInputFormats = ['M!/d!/yyyy'];

	$scope.popup1 = {
	opened: false
	};

	$scope.popup2 = {
	opened: false
	};

	var tomorrow = new Date();
	tomorrow.setDate(tomorrow.getDate() + 1);
	var afterTomorrow = new Date();
	afterTomorrow.setDate(tomorrow.getDate() + 1);
	$scope.events =
	[
	  {
		date: tomorrow,
		status: 'full'
	  },
	  {
		date: afterTomorrow,
		status: 'partially'
	  }
	];

	$scope.getDayClass = function(date, mode) {
	if (mode === 'day') {
	  var dayToCheck = new Date(date).setHours(0,0,0,0);

	  for (var i = 0; i < $scope.events.length; i++) {
		var currentDay = new Date($scope.events[i].date).setHours(0,0,0,0);

		if (dayToCheck === currentDay) {
		  return $scope.events[i].status;
		}
	  }
	}

	return '';
	};

	$scope.options = {
		country: 'ca',
		types: 'geocode',
	};

	// $scope.users = addressServ.query();

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
mainCtrl.$inject = ['$scope'];

// MAIN //
angular
	.module('delivery', [
		'ngAutocomplete',
		'ui.bootstrap',
		'ngResource'
	])

	.config(config)
	.controller('mainCtrl', mainCtrl)
	// .factory('addressServ', addressServ)
