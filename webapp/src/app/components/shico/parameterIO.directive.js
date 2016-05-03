(function() {
  'use strict';

  angular
    .module('shico')
    .directive('parameterIo', parameterIO);

  function parameterIO() {
      var directive = {
          scope: {},    // Directive has it's own personal scope
          templateUrl: 'app/components/shico/parameterIO.template.html',
          controllerAs: 'vm',
          controller: 'ParameterIOController'
      };
      return directive;
  }
})();
