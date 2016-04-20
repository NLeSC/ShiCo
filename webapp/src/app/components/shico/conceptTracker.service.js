(function() {
  'use strict';

  angular
      .module('shico')
      .service('ConceptService', ConceptService);

  function ConceptService($resource, $log, SettingsService) {
    var service = {
      trackConcept: trackConcept
    };
    return service;

    function trackConcept(trackerParams) {
      var tracker = $resource(SettingsService.trackerURL);
      var request = tracker.get(trackerParams);
      var trackPromise = request.$promise.then(parseTermTrack);
      return trackPromise;
    }

    function parseTermTrack(data) {
      // If data needs to be parsed, it should be done here.

      // Copy year into each node
      angular.forEach(data.networks, function(net,year) {
        angular.forEach(net.nodes, function(node) {
          node.year = year;
        });
      });
      return data.toJSON();
    }
  }
})();
