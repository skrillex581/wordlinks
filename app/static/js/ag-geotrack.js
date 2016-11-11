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


        var app = angular.module('geotracker', ['openlayers-directive']);

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

        /* controller demo for geoJSON */
        app.controller('GeoJSONController', ['$rootScope', '$http', 'olData',
            function($rootScope, $http, olData) {
                //get the list of co-ordinates
                //set the center to the middle point in this list.                

                angular.extend($rootScope, {
                        mymapcentre: {
                            lat: -33.918861,
                            lon: 18.423300,
                            zoom: 3
                        },
                        geojson: {
                            name: 'japan',
                            source: {
                                type: 'GeoJSON',
                                url: '/static/data/jpn.json'
                            }
                        }
                    }

                );
            }

        ]);
        /* controller mapactions */

        app.controller('mapactions', function($scope, $rootScope, $http, olData) {
            //default
            angular.extend($rootScope, {
                mymapcentre: {
                    lat: -33.918861,
                    lon: 18.423300,
                    zoom: 15
                },
                iternary: {
                    name: 'TravelPath',
                    source: {
                        type: 'GeoJSON',
                        url: '/static/data/jpn.json'
                    }
                }
            });

            $http.get('/geotracker/getupdatedays').then(
                function(response) {
                    $scope.data = response.data;
                    console.log($scope.data);
                    $scope.data.push({
                        "Count": 100,
                        "Date": "2015-01-02"
                    });
                    $scope.data.push({
                        "Count": 100,
                        "Date": "2015-01-04"
                    });
                },
                function(response) {
                    console.log(response.statusText)
                });

            $scope.ondateclick = function(dt) {

                var sourceTemplate = {
                    type: 'GeoJSON',
                    geojson: {
                        projection: 'EPSG:3857',
                        object: {}
                    }
                };
                $http.get('/geotracker/getpositiondatabyday/' + dt + '/20/').then(
                    function(response) { //jan 2, jan 4 2015
                        $scope.positiondata = response.data;
                        var mp = response.data[Math.floor(response.data.length - 1)]; //centre on last position                                                
                        angular.extend($rootScope, {
                            mymapcentre: {
                                lat: parseFloat(mp.Latitude),
                                lon: parseFloat(mp.Longitude),
                                zoom: 15
                            }
                        });
                    },
                    function() {
                        console.log('some kind of error');
                    });
                $http.get('/geotracker/getpositiondatabydayasgeojson/' + dt + '/20/app.json').then(
                    function(successdata) {
                        $scope.iternary.source = angular.copy(sourceTemplate);
                        console.log($scope.iternary.source.clear());
                        $scope.iternary.source.geojson.object = successdata;
                    },
                    function(errordata) {
                        console.log('something went wrong getting map lines');
                    }
                );

                //end
                //console.log(response.data);
                console.log($scope.mymapcentre);
            };
        });

        /* controller approvals */

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




    }

)();