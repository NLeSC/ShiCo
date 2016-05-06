(function() {
  'use strict';

  angular
    .module('shico')
    .directive('trackerParameters', trackerParameters);

  function trackerParameters() {
      var directive = {
          scope: {},    // Directive has it's own personal scope
          templateUrl: 'app/components/shico/trackerParameters.template.html',
          controllerAs: 'vm',
          controller: 'TrackerParametersController'
      };
      return directive;
  }
})();
