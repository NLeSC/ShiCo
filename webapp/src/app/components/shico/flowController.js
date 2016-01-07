(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FlowController', FlowController);

  function FlowController(ConceptService, GraphConfigService) {
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

    vm.streamGraph = {
      options: GraphConfigService.getConfig('streamGraph'),
      data:    []
    };

    vm.forceGraph = {
      options: GraphConfigService.getConfig('forceGraph'),
      data: [],
      currYearIdx: 0
    };
    vm.yearLabels = [];

    vm.slider_options = {
      floor: 0,
      ceil: 0,
      showTicksValues: true,
      translate: function(value) {
        return vm.yearLabels[value];
      }
    };

    function doPost() {
      var resp = ConceptService.trackConcept(vm.parameters);
      resp.then(function(data) {
        // Collect all words and year labels on data
        var allYears = [];
        var allWords = new Set();
        angular.forEach(data, function(wordValues, year) {
          allYears.push(year);
          angular.forEach(wordValues, function(weight, word) {
            allWords.add(word);
          });
        });

        // Create year idx -> label table
        var yearIdx = {};
        angular.forEach(allYears, function(year, idx) {
          yearIdx[year] = idx;
        });

        // Register year labels with to be used by config
        GraphConfigService.setStreamYears(allYears);
        vm.yearLabels = allYears;

        // Prepare data on format suitable from NVD3
        var streamData = formatForStream(data, yearIdx, allWords, allYears);
        var forceData  = formatForForce(data, yearIdx, allWords, allYears);

        // Register data on graph
        vm.streamGraph.data = streamData;
        vm.forceGraph.data = forceData;

        vm.slider_options.ceil = vm.yearLabels.length-1;
      });
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
