(function() {
    'use strict;'

    function interceptor($rootScope) {
        return {
            request: function(config) {
                console.log('something requested');
                $rootScope.http_busy = true;
                return config;
            },
            requestError: function(config) {
                return config;
            },
            response: function(res) {
                console.log('got a response');
                $rootScope.http_busy = false;
                return res;
            },
            responseError: function(res) {
                return res;
            }
        }
    }

    var app = angular.module('wordgames', []);

    app.service('interceptor', interceptor);


    /* application configuration section */

    app.config(function($httpProvider) {
        $httpProvider.interceptors.push('interceptor');
    });

    /* run on app initialisation (like a constructor) */

    app.run(function($http, $rootScope) {
        //on app initial run    
        $rootScope.http_busy = false;
    });



    /* controller approvals */
    app.controller('wordladdercontroller', function($scope, $http) {
        $scope.getwordladder = function(start, end) {
            $http.get('http://localhost:5000/wordsapi/v1.0/words/ladder/' + start + '/' + end + '/').then(
                function(response) {
                    console.log(response.data)
                    $scope.words = response.data.words;
                    console.log($scope.words)
                },
                function(response) {
                    console.log(response.data.error)
                });
            return false;
        }
        $scope.getanagrams = function(myword) {
            $http.get('http://localhost:5000/wordsapi/v1.0/words/anagram/' + myword + '/').then(
                function(response) {
                    console.log(response.data)
                    $scope.words = response.data.words;
                    console.log($scope.words)
                },
                function(response) {
                    console.log(response.data.error)
                });
            return false;
        }
    });
    app.controller('approvals', function($scope, $http) {
        $http.get('/geotracker/getapprovalslist').then(
            function(response) {
                $scope.data = response.data;
            },
            function(response) {
                console.log(response.statusText)
            });
        $scope.onclick = function(id) {
            $http.get('/geotracker/approve/' + id + '/').then(
                function(response) {
                    console.log('Approval success.');
                    for (var i = 0; i < $scope.data.length; i++) {
                        if ($scope.data[i].Id == id) {
                            $scope.data.splice(i, 1);
                        }
                    }
                },
                function(response) {
                    console.log('Approval failure.')
                });
        }
    });

    /* app directives */
    app.directive('mymap', function() {
        return {
            restrict: "E",
            template: "<h1>hello world</h1>"
        }
    });
})();