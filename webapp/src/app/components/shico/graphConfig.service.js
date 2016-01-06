(function() {
  'use strict';

  angular
      .module('shico')
      .service('GraphConfigService', GraphConfigService);

  function GraphConfigService() {
    // TODO: streamConfig could be loaded from JSON ?
    // NVD3 configuration for stream graph
    var streamConfig = {
      chart: {
          type: 'stackedAreaChart',
          height: 400,
          margin : {
              top: 20,
              right: 20,
              bottom: 60,
              left: 55
          },
          x: getX,
          y: getY,
          xAxis: {
            tickFormat: tickYear
          },
          yAxis: {
            tickFormat: tickY
          }
      }
    };
    // TODO: forceConfig could be loaded from JSON ?
    // NVD3 configuration for force directed graph
    var forceConfig = {
      chart: {
          type: 'forceDirectedGraph',
          height: 300,
          width: 300,
          color: d3.scale.category20(),
          radius: 5,
          nodeExtras: addTextLabels
      }
    };

    var yearTickLabels = {};   // Year markers for stream graph

    var service = {
      getConfig: getConfig,
      setStreamYears: setStreamYears
    };
    return service;

    // Helper functions for streamConfig
    function getX(point){ return point[0]; }
    function getY(point){ return point[1]; }
    function tickY(tickVal) { return parseFloat(tickVal).toFixed(1); }

    function tickYear(idx) {
      if(idx in yearTickLabels) { return yearTickLabels[idx]; }
      else { return idx; }
    }
    function setStreamYears(labels) {
      yearTickLabels = labels;
    }

    // Helper functions for forceConfig
    function addTextLabels(node) {
      node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });
    }

    function getConfig(graphName) {
      if(graphName === 'streamGraph') {
        return streamConfig;
      } else if(graphName === 'forceGraph'){
        return forceConfig;
      }
    }
  }
})();
