(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerParametersController', TrackerParametersController);

  function TrackerParametersController(TrackerParametersService) {
    var vm = this;
    vm.algorithms = ['Adaptive', 'Non-adaptive'];
    vm.weighFuncs = ['Gaussian', 'Linear', 'JSD'];
    vm.directions = ['Forward', 'Backward'];
    vm.boostMethods = ['Sum similarity', 'Counts'];
    vm.doCleaning = [ 'Yes', 'No' ];

    // Years and features gets loaded by SettingsService
    vm.years = TrackerParametersService.availableYears;
    vm.features = TrackerParametersService.features;

    // We use the parameters variable from ParameterService directly.
    vm.parameters = TrackerParametersService.getParameters();

    //
    vm.tooltips = TrackerParametersService.tooltips;
  }
})();
