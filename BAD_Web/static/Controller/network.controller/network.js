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

app.controller('network.ejemplo', function ($http, $scope, $filter, $timeout, $compile) {

  $scope.prueba = "hola"
  $scope.hola = "inicio con esta palabra"
  $scope.list_upload = []
  $scope.prueba_funcion = function(){
    alert("hola")
  }
  var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');

  reload_table()



  Dropzone.options.dropzoneuploadimage = {
    url: "/network/upload_images/",
    paramName: "file", // The name that will be used to transfer the file
    maxFilesize: 2, // MB
    accept: function(file, done) {
      location.reload()
      if (file.name == "justinbieber.jpg") {
        done("Naha, you don't.");
      }
      else { done(); }
    }
  };

/*
  $(document).ready(function() {
    $('#table_upload').DataTable( {
        deferRender:    true,
        scrollY:        200,
        scrollCollapse: true,
        scroller:       true
    } );
} );
*/
  function reload_table (){

    var req = {
      method: 'POST',
      url: '/network/get_upload_list/',
      headers: {
        "X-CSRFToken": $crf_token
      }
    }

    $http(req)
      .success(function(response){
          $scope.list_upload = response.file_list
          console.log($scope.list_upload)
      })
    }

    $scope.process = function(id_upload){
      var req = {
      method: 'POST',
      url: '/network/process/',
      headers: {
        "X-CSRFToken": $crf_token
      },
      data: { id: id_upload,
          multi_start: false
          }
      }

      $http(req)
        .success(function(response){
          alert(response.status)
          location.reload()
        })


    }



})

  