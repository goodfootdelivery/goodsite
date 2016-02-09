/**
 * Confirm Controller for Modal Confirmation
 *
 * 					Wed  3 Feb 17:07:35 2016
 *
 * @ngInject
 */
confirmCtrl = function($uibModalInstance, orderServ, pmap, dmap){
	var self = this;

	// maps
	self.pmap = pmap;
	self.dmap = dmap;

	//marks
	self.pmark = {
		id: 0,
		coords: pmap.center,
	};
	self.dmark = {
		id: 1,
		coords: dmap.center,
	};

	// Open & Close
	self.ok = function () {
		$uibModalInstance.close();
	};

	self.cancel = function () {
		$uibModalInstance.close();
	}
};
// confirmCtrl.$inject = ['$uibModalInsatnce'];

