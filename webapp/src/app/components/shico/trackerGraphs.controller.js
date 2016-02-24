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
    vm.downloadData = downloadData;

    function downloadData() {
      console.log('Start data download...');
      console.log('vm.streamGraph.data');
      console.log(vm.streamGraph.data);
      console.log('vm.forceGraph.data');
      console.log(vm.forceGraph.data);

      return ['x','y','z'];
    }
  }
})();
