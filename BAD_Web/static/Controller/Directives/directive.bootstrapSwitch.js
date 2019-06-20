/*

MachineLearning for Early-Alert System project.

Created by Brayan Rojas, Elkin Prada, on June 2019.
Co-workers: Carlos Sierra, Santiago Salazar
Copyright (c) 2019 Brayan Rojas, Elkin Prada Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.

*/
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