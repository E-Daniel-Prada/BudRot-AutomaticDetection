app.directive('bootstrapswitch', ['$timeout', function($timeout) {
	return {
		restrict: 'EA',
		require: '?ngModel',
		scope: {
			model: '=ngModel',
			disabled:'=ngDisabled'
		},
		link: function($scope, $element, $attrs, ngModel) {

			$timeout(function() {
				if (!$element.hasClass('make-switch')) {
					if($attrs.size){
						$element.addClass('make-switch switch-'+$attrs.size)
					}else{
						$element.addClass('make-switch has-switch')
					}
					
					$element.bootstrapSwitch({});
				}
				//ngModel.$setViewValue($element.bootstrapSwitch('status', false));
				$element.on('switch-change', function(e, data) {
					if (ngModel) {
						ngModel.$setViewValue(data.value);
					}
				})

				$scope.$watch('disabled', function(newValue, oldValue) {
					console.log(newValue, oldValue)
					$element.bootstrapSwitch('setActive', !newValue)
				});

				$scope.$watch('model', function(newValue, oldValue) {
					console.log(newValue, oldValue)
					if (newValue) {

						
						$timeout(function() {
							$element.bootstrapSwitch('setState', newValue)
						})
					}
				}, true);


			});
		}
	};
}]);