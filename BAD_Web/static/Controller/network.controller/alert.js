/*

MachineLearning for Early-Alert System project.

Created by Brayan Rojas, Elkin Prada, on June 2019.
Co-workers: Carlos Sierra, Santiago Salazar
Copyright (c) 2019 Brayan Rojas, Elkin Prada Corporación Universitaria Minuto de Dios. All rights reserved.

This file is part of ProjectName (BudRot-AutomaticDetection).

ProjectName (BudRot-AutomaticDetection) is free software: you can redistribute it and/or modify it under the terms of the
GNU General Public License as published by the Free Software Foundation, version 3.

*/


var app = angular.module('app',[]);
app.run(function($http) {

  token = localStorage.getItem('token');
  $http.defaults.headers.common.Authorization = 'Token ' + token;

});
app.controller('network.alert', function ($http, $scope, $filter, $timeout, $compile) {

  $scope.user_list = []
  var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


  reload_table()


  function reload_table (){

    var req = {
      method: 'GET',
      url: '/network/get_alert_list/',
      headers: {
        "X-CSRFToken": $crf_token
      }
    }

    $http(req)
      .success(function(response){
          $scope.alert_list = response.file_list
          console.log($scope.alert_list)
      })
    }



})

  