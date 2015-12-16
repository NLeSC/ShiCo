(function() {
  'use strict';

  angular
      .module('shico')
      .controller('FlowController', FlowController);

  function FlowController(ConceptService, GraphConfigService) {
    var vm = this;

    vm.doPost = doPost;
    vm.doPrint = doPrint;
    vm.parameters = {
      terms: 'oorlog',
      maxTerms: 5,
      sumDistances: true
    };
    vm.results = {
      graph1: '',
      grahp2: ''
    };

    vm.graph = {
      options: getGraphOptions(),
      data:    getGraphData(1)
    };

    function getGraphOptions() {
      var loader = GraphConfigService.getConfig();
      loader.then(function(data) {
        console.log('Got your config, as promised!');
        console.log(data);
      });
      return {
        chart: {
            type: 'stackedAreaChart',
            height: 450,
            margin : {
                top: 20,
                right: 20,
                bottom: 60,
                left: 55
            },
            x: function(d){ return d[0]; },
            y: function(d){ return d[1]; },
            xAxis: {
              tickFormat: function(d) { return d + '_'; }
            }
        }
      };
    }

    function getGraphData(factor) {
      return [
        {
            "key" : "bevrijding",
            "values" : [ [ 1950 , factor*1] , [ 1951 , 0] ]
        },
        {
            "key" : "wereldoorlog",
            "values" : [ [ 1950 , factor*1] , [ 1951 , 0] ]
        },
        {
            "key" : "oorlogen",
            "values" : [ [ 1950 , factor*1] , [ 1951 , 1] ]
        },
        {
            "key" : "burgeroorlog",
            "values" : [ [ 1950 , factor*3] , [ 1951 , 1] ]
        }
      ];
    }

    function doPost() {
      var resp = ConceptService.trackConcept(vm.parameters);

      console.log("DoPost of: ");
      console.log(vm.parameters);

      resp.then(function(data) {
        console.log('Data returned by service');
        console.log(data);

        vm.results.graph1 = data['1951_1960'][0][0];
        vm.results.graph2 = 'Blue';

        vm.graph.data = getGraphData(3);
      });
    }

    function doPrint() {
      console.log("Do print of: ");
      console.log(vm.parameters);
    }
  }
})();
