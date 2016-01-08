(function() {
  'use strict';

  angular
    .module('shico')
    .controller('TrackerGraphsController', TrackerGraphsController);

  function TrackerGraphsController(GraphControlService) {
    var vm = this;

    // Share graph data from service to controller
    // so directive can find them.
    vm.streamGraph = GraphControlService.streamGraph;
    vm.forceGraph = GraphControlService.forceGraph;
    vm.slider_options = GraphControlService.slider_options;
  }
})();
