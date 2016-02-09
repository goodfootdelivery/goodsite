/**
 * Date Form Directive
 * 		Fri 29 Jan 18:11:42 2016
 */

dateForm = function(){
	return {
		restrict: 'A',
		bindToController: {
			date: '=?',
			time: '=?'
		},
		controller: function(){
			var self = this;

			self.today = function() {
				self.date = new Date();
				self.time = new Date();
			};
			self.today();

			self.clear = function() {
				self.date = null;
			};

			// Disable weekend selection
			self.disabled = function(date, mode) {
				return mode === 'day' && (date.getDay() === 0 || date.getDay() === 6);
			};

			self.toggleMin = function() {
				self.minDate = self.minDate ? null : new Date();
			};

			self.toggleMin();
			self.maxDate = new Date(2020, 5, 22);

			self.open = function() {
				self.popup.opened = true;
			};

			self.setDate = function(year, month, day) {
				self.date = new Date(year, month, day);
			};

			self.dateOptions = {
				formatYear: 'yy',
				startingDay: 1
			};

			self.formats = ['dd-MMMM-yyyy', 'yyyy/MM/dd', 'dd.MM.yyyy', 'shortDate'];
			self.format = self.formats[0];
			self.altInputFormats = ['M!/d!/yyyy'];

			self.popup = {
				opened: false
			};

			var tomorrow = new Date();
			tomorrow.setDate(tomorrow.getDate() + 1);

			var afterTomorrow = new Date();
			afterTomorrow.setDate(tomorrow.getDate() + 1);

			self.events = [
				{ date: tomorrow, status: 'full' },
				{ date: afterTomorrow, status: 'partially' }
			];

			self.getDayClass = function(date, mode) {
				if (mode === 'day') {
						var dayToCheck = new Date(date).setHours(0,0,0,0);

					for (var i = 0; i < self.events.length; i++) {
						var currentDay = new Date(self.events[i].date).setHours(0,0,0,0);

						if (dayToCheck === currentDay) {
						  return self.events[i].status;
						}
					}
				}
				return '';
			};
		},
		controllerAs: 'dm',
		templateUrl: '/static/views/dateForm.html'
	}
}
