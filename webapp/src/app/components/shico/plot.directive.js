(function() {
  'use strict';

  angular
    .module('shico')
    .directive('plotDirective', plotDirective);

  function plotDirective() {
    var directive = {
      scope: {},    // Directive has it's own personal scope
      templateUrl: '/app/components/shico/plotDirective.template.html',
      controllerAs: 'vm',
      controller: 'PlotDirectiveController'
    };
    return directive;
  }

  angular
    .module('shico')
    .controller('PlotDirectiveController', PlotDirectiveController);

  function PlotDirectiveController(GraphControlService) {
    var vm = this;

    // Share graph data from service to controller
    // so directive can find them.
    vm.streamGraph = GraphControlService.streamGraph;
    vm.forceGraph = GraphControlService.forceGraph;

    vm.slider_options = GraphControlService.slider_options;
  }

})();
