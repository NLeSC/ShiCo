(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FlowController', FlowController);

  function FlowController(ConceptService,
                          GraphControlService) {
    var vm = this;

    // FlowController exposed functions
    vm.doPost = doPost;
    //    TODO: move do paramIO controller
    vm.getParameters = getParameters;
    vm.setParameters = setParameters;
    vm.closeParamIO = closeParamIO;

    // FlowController exposed variables
    vm.parameters = {
      terms: 'oorlog',
      maxTerms: 5,
      sumDistances: true
    };

    // TODO: move to paramIO controller
    vm.paramIOControl = {
      text: 'xxx',
      readOnly: false,
      hide: true
    };

    // Share graph data from service to controller
    // so directive can find them.
    vm.streamGraph = GraphControlService.streamGraph;
    vm.forceGraph = GraphControlService.forceGraph;
    vm.slider_options = GraphControlService.slider_options;

    function doPost() {
      var resp = ConceptService.trackConcept(vm.parameters);
      // resp.then(GraphControlService.doSomething);
      resp.then(GraphControlService.update);
    }

    // TODO Move formatForStream and formatForForce to
    // a service and create an independant controller for
    // plot directive which only reads from that service
    function formatForStream(data, yearIdx, allWords, allYears) {
      var streamData = [];
      angular.forEach(allWords, function(word) {
        var values = [];
        angular.forEach(allYears, function(year) {
          var val = (word in data[year]) ? data[year][word] : 0;
          this.push([ yearIdx[year], val]);
        }, values);
        this.push({
          key: word,
          values: values
        });
      }, streamData);
      return streamData;
    }

    function formatForForce(data, yearIdx, allWords) {
      var forceData = {};

      angular.forEach(data, function(wordValues, year) {
        var yearForceData = {};
        yearForceData.links = [];
        yearForceData.nodes = [];
        yearForceData.nodes.push({ name: '' });
        var n = 1;
        angular.forEach(wordValues, function(weight, word) {
          yearForceData.nodes.push({ name: word });
          yearForceData.links.push({
            source: 0,
            target: n,
            value:  weight
          });
          n = n + 1;
        });
        forceData[yearIdx[year]] = yearForceData;
      });

      return forceData;
    }

    // TODO Move getParameters and setParameters to
    // a service and create an independant controller for
    // parameterIO directive which only uses that service
    function getParameters() {
      vm.paramIOControl.hide = false;
      vm.paramIOControl.readOnly = true;
      vm.paramIOControl.text = JSON.stringify(vm.parameters);
      vm.paramIOControl.btnText = 'Ok';
    }

    function setParameters() {
      vm.paramIOControl.hide = false;
      vm.paramIOControl.readOnly = false;
      vm.paramIOControl.text = '';
      vm.paramIOControl.btnText = 'Load';
    }

    function closeParamIO() {
      vm.paramIOControl.hide = true;
      if(!vm.paramIOControl.readOnly) {
        vm.parameters = JSON.parse(vm.paramIOControl.text);
      }
    }
  }
})();
