(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerParametersController', TrackerParametersController);

  function TrackerParametersController($scope, $timeout, TrackerParametersService) {
    var vm = this;

    // Values for dropdown items
    vm.algorithms = ['Adaptive', 'Non-adaptive'];
    vm.weighFuncs = ['Gaussian', 'Linear', 'JSD'];
    vm.directions = ['Forward', 'Backward'];
    vm.boostMethods = ['Sum similarity', 'Counts'];
    vm.doCleaning = [ 'Yes', 'No' ];

    // Open/close advanced parameters section
    vm.isOpen = false;

    // We use variables from TrackerParametersService directly.
    vm.years = TrackerParametersService.availableYears;
    vm.features = TrackerParametersService.features;
    vm.parameters = TrackerParametersService.getParameters();
    vm.tooltips = TrackerParametersService.tooltips;

    // Expose functions
    vm.toggleOpen = toggleOpen;

    function toggleOpen() {
      vm.isOpen = !vm.isOpen;
      $timeout(function () {
        // Force redraw of slider
        $scope.$broadcast('rzSliderForceRender');
      }, 500); // Wait 500 ms before triggering redraw
    }
  }
})();
