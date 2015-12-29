(function(){
	// Change Angular tags
	$interpolateProvider.startSymbol('[[').endSymbol(']]');
	$resourceProvider.defaults.stripTrailingSlashes = false;

	var app = angular.module('Order', ['ng.django.forms']);
})
