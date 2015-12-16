(function() {
  'use strict';

  angular
      .module('shico')
      .service('ConceptService', ConceptService);

  function ConceptService($resource, $log) {
    var service = {
      trackConcept: trackConcept
    };
    return service;

    function trackConcept(trackerParams) {
      // var tracker = $resource('http://localhost:5000/track/:terms');
      var tracker = $resource('dummy.json');
      var request = tracker.get(trackerParams, parseTermTrack);
      return request.$promise;
    }

    function parseTermTrack(data) {
      $log.debug('ConceptService returned data!');
      // If data needs to be post-processed, do so here
      delete data['$promise'];
      delete data['$resolved'];
    }
  }
})();
