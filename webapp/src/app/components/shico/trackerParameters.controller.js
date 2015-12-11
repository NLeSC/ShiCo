(function() {
  'use strict';

  angular
      .module('shico')
      .controller('trackerParametersController', trackerParametersController);

  function trackerParametersController($log) {
    var vm = this;
    vm.getData = getData;

    function getData() {
      $log.debug('Returning data from the form...');
      var trackerParams = {
        'terms': 'vm.terms',
        'maxTerms': 5,
        'sumDistances': true
        // Add more parameters for /track here...
      };
      return trackerParams;
    }
  }
})();
