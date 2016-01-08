(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerParametersController', TrackerParametersController);

  function TrackerParametersController(TrackerParametersService) {
    var vm = this;

    // We use the parameters variable from ParameterService directly.
    vm.parameters = TrackerParametersService.getParameters();
  }
})();
