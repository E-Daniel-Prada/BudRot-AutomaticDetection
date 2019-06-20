app.directive('select2', ['$timeout', function($timeout) {
	return {
		restrict: 'EA',
		require: '?ngModel',
		scope: {
			model: '=ngModel'
		},
		link: function($scope, $element, $attrs, ngModel) {
			if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
				minimumResultsForSearch = -1
			} else {
				minimumResultsForSearch = 1
			}
			$timeout(function() {
				$element.css('width', '100%')
				$element.select2({
					minimumResultsForSearch: minimumResultsForSearch,
					placeholder: $attrs.placeholder
				});
				if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
					$element.on('select2:opening select2:closing', function(event) {
						$(this).parent().find('.select2-search__field').prop('disabled', true);
					});
				}
				$element.on('change', function(e) {
					if (ngModel) {
						ngModel.$setViewValue($element.val());
					}

				})
				$scope.$watch('model', function(newValue, oldValue) {
					if (newValue) {
						$timeout(function() {
							$element.val(newValue).trigger('change')
						})
					}
				}, true);
			});
		}
	};
}]);