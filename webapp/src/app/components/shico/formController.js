(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FormController', FormController);

  function FormController($log, $resource) {
    var vm = this;
    vm.submit = submit;

    // Fetch data from form and send it to tracker service
    function submit() {
      var trackerParams = fetchData();
      queryTrackerService(trackerParams);
    }

    // Fetch data from form
    function fetchData() {
      var trackerParams = {
        'terms': vm.terms,
        'maxTerms': 5,
        'sumDistances': true
        // Add more parameters for /track here...
      };
      return trackerParams;
    }

    // Load data into form
    function loadData(trackerParams) {
      vm.terms = trackerParams['terms'];
      // Add more parameters for /track here...
    }

    //
    function queryTrackerService(trackerParams) {
      // var tracker = $resource('http://localhost:5000/track/:terms');
      var tracker = $resource('dummy.json');
      tracker.get(trackerParams, parseTermTrack);
    }

    function parseTermTrack(data) {
      $log.debug('Found data!');
      $log.debug(data);
    }
  }
})();
