(function() {
  'use strict';

  angular
      .module('shico')
      .service('SettingsService', SettingsService);

  function SettingsService($resource) {
    var service = {
      doLoad: doLoad,
    };
    return service;

    function doLoad() {
      var configFile = $resource('config.json');
      configFile.get().$promise.then(function(config) {

        // Copy config from JSON to the service
        service.trackerURL = config.trackerURL;
      });
    }
  }
})();
