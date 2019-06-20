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

  