/**
 * Address Form Directive
 * Wed 27 Jan 21:27:02 2016
 */

addressForm = function(){
	return {
		restrict: 'A',
		scope: {
			address: '=?',
			check: '&'
		},
		templateUrl: '/static/views/addressForm.html'

	}
}

