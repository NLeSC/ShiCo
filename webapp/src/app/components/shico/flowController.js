(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FlowController', FlowController);

  function FlowController(ConceptService,
                          GraphControlService,
                          TrackerParametersService) {
    var vm = this;

    // FlowController exposed functions
    vm.doPost = doPost;

    // Share graph data from service to controller
    // so directive can find them.
    vm.streamGraph = GraphControlService.streamGraph;
    vm.forceGraph = GraphControlService.forceGraph;
    vm.slider_options = GraphControlService.slider_options;

    function doPost() {
      var params = TrackerParametersService.getParameters();
      var resp = ConceptService.trackConcept(params);
      resp.then(GraphControlService.update);
    }
  }
})();
