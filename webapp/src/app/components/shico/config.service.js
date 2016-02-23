(function() {
  'use strict';

  angular
      .module('shico')
      .service('SettingsService', SettingsService);

  function SettingsService($resource, TrackerParametersService) {
    var service = {
      doLoad: doLoad
    };
    return service;

    function doLoad() {
      var configFile = $resource('config.json');
      configFile.get().$promise.then(function(config) {
        var baseURL = config.baseURL;
        var trackerURL = baseURL + '/track/:terms';
        var avlYearSvcURL = baseURL + '/available-years';

        if(baseURL.length==0) {
          trackerURL = 'dummy2.json';
          avlYearSvcURL = 'http://localhost:5000/available-years';
        }

        // Copy config from JSON to the service
        service.trackerURL = trackerURL;

        // Call avlYearSvc resource to get years
        var avlYearResource = $resource(avlYearSvcURL);
        avlYearResource.get().$promise.then(function(years) {
          TrackerParametersService.availableYears.from = years.first;
          TrackerParametersService.availableYears.to = years.last;
          TrackerParametersService.availableYears.values = years.values;
          TrackerParametersService.availableYears.options.floor = years.first;
          TrackerParametersService.availableYears.options.ceil = years.last;
        });
      });
    }
  }
})();
