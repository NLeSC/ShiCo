(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FormController', FormController);

  function FormController(ConceptService,
                          TrackerParametersService,
                          GraphControlService) {
    var vm = this;

    vm.doPost = doPost;

    function doPost() {
      var params = TrackerParametersService.getParameters();
      var resp = ConceptService.trackConcept(params);
      resp.then(GraphControlService.update);
    }
  }
})();
