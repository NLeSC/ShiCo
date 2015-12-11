(function() {
  'use strict';

  angular
      .module('shico')
      .directive('trackerParameters', trackerParameters);

  function trackerParameters() {
      var directive = {
          templateUrl: '/app/components/shico/trackerParameters.template.html',
          controller: 'trackerParametersController',
      };
      return directive;
  }
})();
