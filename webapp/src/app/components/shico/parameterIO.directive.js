(function() {
  'use strict';

  angular
    .module('shico')
    .directive('parameterIo', parameterIO);

  function parameterIO() {
      var directive = {
          templateUrl: '/app/components/shico/parameterIO.template.html',
      };
      return directive;
  }
})();
