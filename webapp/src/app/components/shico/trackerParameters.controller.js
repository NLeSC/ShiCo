(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerParametersController', TrackerParametersController);

  function TrackerParametersController(TrackerParametersService) {
    var vm = this;
    vm.algorithms = ['inlinks', 'outlinks', 'non-adaptive'];
    vm.weighFuncs = ['Gaussian', 'Linear', 'JSD'];
    // Years not defined  here because it gets loaded by service
    vm.years = TrackerParametersService.availableYears;

    // We use the parameters variable from ParameterService directly.
    vm.parameters = TrackerParametersService.getParameters();
  }
})();
