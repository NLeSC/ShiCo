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
          },
          color: getColour,
      }
    };
    // TODO: forceConfig could be loaded from JSON ?
    // NVD3 configuration for force directed graph
    var forceConfig = {
      chart: {
          type: 'forceDirectedGraph',
          height: 300,
          width: 300,
          // color: d3.scale.category20(),
          color: getColour,
          radius: 5,
          nodeExtras: processNode
      }
    };
    var colours = d3.scale.category20();

    var yearTickLabels = {};   // Year markers for stream graph
    var forceGraphHooks = [];
    var wordColourIdx = {};

    var service = {
      getConfig: getConfig,
      setStreamYears: setStreamYears,
      addForceGraphHook: addForceGraphHook,
      setVocabulary: setVocabulary
    };
    return service;

    // Helper functions for all graphs
    function setVocabulary(vocab) {
      var idx = 0;
      // Each word of vocabulary is assigned an unique ID, later used to assign colour
      // TODO: can't we get a list of words from server?
      angular.forEach(vocab, function(word) {
        wordColourIdx[word] = idx;
        idx += 1;
      });
    }

    function getColour(item) {
      var word = item.key || item.name;
      var cIdx = wordColourIdx[word];
      return cIdx ? colours(cIdx) : '#223344';
    }

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
    function processNode(node) {
      addTextLabels(node);
      angular.forEach(forceGraphHooks, function(hook) {
        hook(node);
      });
    }

    function addTextLabels(node) {
      node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; });
    }

    function addForceGraphHook(callback) {
      forceGraphHooks.push(callback);
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
