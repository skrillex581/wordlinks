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
    //https://appendto.com/2016/02/working-promises-angularjs-services/
    function wordServiceAPI($http, $q) {
        var deferred = $q.defer();
        this.GetAnagrams = function(word) {
            return $http.get('http://127.0.0.1:5000/wordsapi/v1.0/words/anagram/' + word + '/')
                .then(function(response) {
                        deferred.resolve(response.data);
                        return deferred.promise;
                    },
                    function(response) {
                        deferred.reject(response);
                        return deferred.promise;
                    });
        }
        this.GetWordLadder = function(start, end) {
            return $http.get('http://127.0.0.1:5000/wordsapi/v1.0/words/getladder/' + start + '/' + end + '/')
                .then(function(response) {
                        //promise is fulfilled
                        deferred.resolve(response.data);
                        //promise is resolved
                        return deferred.promise;
                    },
                    function(response) {
                        //the followig line rejects the promise
                        deferred.reject(response);
                        return deferred.promise;
                    });
        }
    }

    var app = angular.module('wordgames', []);

    app.service('interceptor', interceptor); //inject srevices
    app.service('WordGameAPI', wordServiceAPI)

    /* application configuration section */

    app.config(function($httpProvider) {
        $httpProvider.interceptors.push('interceptor');
        //todo: configure base url for api calls
    });

    /* run on app initialisation (like a constructor) */

    app.run(function($http, $rootScope) {
        //on app initial run    
        $rootScope.http_busy = false;
    });



    /* controller approvals */
    app.controller('wordladdercontroller', function($scope, $http, WordGameAPI) {
        $scope.getwordladder = function(start, end) {
            WordGameAPI.GetWordLadder(start, end)
                .then(function(result) {
                        console.log(result.words);
                        $scope.data = result;
                    },
                    function(error) {
                        console.log(error.statusText);
                    });
        }


        $scope.getanagrams = function(myword) {
            WordGameAPI.GetAnagrams(myword)
                .then(function(result) {
                        console.log(result.words);
                        $scope.data = result;
                    },
                    function(error) {
                        console.log(error.statusText);
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