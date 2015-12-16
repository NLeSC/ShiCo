(function() {
  'use strict';

  angular
      .module('shico')
      .service('GraphConfigService', GraphConfigService);

  function GraphConfigService($resource, $log) {
    var service = {
      getConfig: getConfig
    };
    return service;

    function getConfig(graphName) {
      console.log('Your config shall be loaded!');
      var tracker = $resource('app/nvd3-config/stream.json');
      // var tracker = $resource('dummy.json');
      var request = tracker.get();
      return request.$promise;
    }
  }
})();
