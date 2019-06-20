var app = angular.module('app',[]);
app.run(function($http) {

  token = localStorage.getItem('token');
  $http.defaults.headers.common.Authorization = 'Token ' + token;

});
app.controller('user.user_registration', function ($http, $scope, $filter, $timeout, $compile) {

  $scope.user_list = []
  var $crf_token = $('[name="csrfmiddlewaretoken"]').attr('value');


  reload_table()


  function reload_table (){

    var req = {
      method: 'GET',
      url: '/user/get_user_list/',
      headers: {
        "X-CSRFToken": $crf_token
      }
    }

    $http(req)
      .success(function(response){
          $scope.user_list = response.file_list
          console.log($scope.user_list)
      })
    }

    $scope.add_user = function(){
      $("#modal_add_user").modal('show')

    }

    $scope.save_user = function(){
      if ($scope.password_one != $scope.password_two){
        alert("las contraseñas no son iguales")
      }else{
        $("#modal_add_user").modal('hide')
        var req = {
        method: 'POST',
        url: '/user/add_user/',
        headers: {
          "X-CSRFToken": $crf_token
        },
        data: { email: $scope.email,
          first_name: $scope.name,
          is_superuser: true,
          last_name: $scope.last_name,
          username: $scope.username,
          password: $scope.password_one
          }
        }

        $http(req)
          .success(function(response){
              alert("transacción exitosa!")
              location.reload()
          })

      }
      
    }


    $scope.edit_user = function(id_user){
      $("#modal_add_user").modal('hide')
        var req = {
        method: 'POST',
        url: '/user/edit_user/',
        headers: {
          "X-CSRFToken": $crf_token
        },
        data: { id: id_user
          }
        }

        $http(req)
          .success(function(response){
              alert("transacción exitosa!")
          })
    }

    $scope.active_user = function(id_user){
      $("#modal_add_user").modal('hide')
        var req = {
        method: 'POST',
        url: '/user/active_user/',
        headers: {
          "X-CSRFToken": $crf_token
        },
        data: { id: id_user
          }
        }

        $http(req)
          .success(function(response){
              alert("transacción exitosa!")
              location.reload()
          })
    }
    var $crf_token2 = $('[name="csrfmiddlewaretoken"]').attr('value');
    $scope.user_remove = function(id_user){
      $("#modal_add_user").modal('hide')
        var req = {
        method: 'POST',
        url: '/user/remove_user/',
        headers: {
          "X-CSRFToken": $crf_token
        },
        data: { id: id_user
              }
        }

        $http(req)
          .success(function(response){
              alert("transacción exitosa!")
              location.reload()
          })
    }
    

  /*
  table = $('#table_user').DataTable( {
                bAutoWidth: false,
                language: {
                        "sProcessing":     '<img src="{% static "images/loading1.gif" %}" height="100" width="100">',
                        "sLengthMenu":     "Mostrar _MENU_ registros",
                        "sZeroRecords":    "No se encontraron resultados",
                        "sEmptyTable":     "Ningún dato disponible en esta tabla",
                        "sInfo":           "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                        "sInfoEmpty":      "Mostrando registros del 0 al 0 de un total de 0 registros",
                        "sInfoFiltered":   "(filtrado de un total de _MAX_ registros)",
                        "sInfoPostFix":    "",
                        "sSearch":         "",
                        "sUrl":            "",
                        "sInfoThousands":  ",",
                        "sLoadingRecords": "Cargando...",
                        "oPaginate": {
                            "sFirst":    "Primero",
                            "sLast":     "Último",
                            "sNext":     "Siguiente",
                            "sPrevious": "Anterior"
                        },
                        "oAria": {
                            "sSortAscending":  ": Activar para ordenar la columna de manera ascendente",
                            "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                        }
                },
                "columns": [
                    {data: "id", className: "center", width: "10%"},
                    {data: "username", width: "15%"},
                    {data: "first_name", width: "15%"},
                    {data: "last_name", width: "15%"},
                    {data: "email", width: "15%"},
                    {data: "is_superuser", width: "15%"},
                    {data: "is_activate", width: "15%"},
                    {data: "last_login", width: "15%"}
                ],
                lengthMenu: [[3, 10, 25], [3, 10, 25]],
                processing: true,
                serverSide: true,
                order: [[ 2, "asc" ]],
                ajax: {
                  url: '/user/get_user_list/',
                  headers: {
                    'Authorization': 'Token ' + localStorage.getItem('token')
                  }
                },
                createdRow: function(row, data, index) {
                  $compile(angular.element(row).contents())($scope);
                },

            } );
*/


})

  