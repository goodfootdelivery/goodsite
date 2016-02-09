/**
 *		Parcel Form Directive
 * 				Mon Feb  1 11:10:26 2016
 */
parcelForm = function(){
	return {
		restrict: 'A',
		bindToController: {
			parcel: '=?',
		},
		controller: function(){
			var self = this;
			// Parcel Sizes
			self.lrg = {"length":3.2, "width":3.2, "height":3.2, "weight":3.2};
			self.sml = {"length":1.2, "width":1.2, "height":1.2, "weight":1.2};
			self.med = {"length":2.2, "width":2.2, "height":2.2, "weight":2.2};
		},
		controllerAs: 'pm',
		templateUrl: '/static/views/parcelForm.html'
	}
}
