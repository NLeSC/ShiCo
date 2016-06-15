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
        var serverSettingsUrl = baseURL + '/load-settings';

        if(baseURL.length==0) {
          trackerURL = 'dummy2.json';
          serverSettingsUrl = 'http://localhost:5000/load-settings';
        }

        // Copy config from JSON to the service
        service.trackerURL = trackerURL;

        // Call serverSettingsUrl resource to server setting
        var serverSettingsResource = $resource(serverSettingsUrl);
        serverSettingsResource.get().$promise.then(function(settings) {
          // Years available
          TrackerParametersService.availableYears.from = settings.years.first;
          TrackerParametersService.availableYears.to = settings.years.last;
          TrackerParametersService.availableYears.values = settings.years.values;
          TrackerParametersService.availableYears.options.floor = settings.years.first;
          TrackerParametersService.availableYears.options.ceil = settings.years.last;

          // Cleaning capabilities
          TrackerParametersService.features.canClean = settings.cleaning;
        });
      });
    }
  }
})();
