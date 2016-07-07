(function() {
  'use strict';

  angular
      .module('shico')
      .service('GraphConfigService', GraphConfigService);

  function GraphConfigService() {
    // NVD3 configuration for stream graph
    var streamConfig = {
      chart: {
          type: 'stackedAreaChart',
          height: 500,
          width: 1000,
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
          color: getColour
      }
    };

    var customSymbol = d3.svg.symbol()
                .type( chooseSymbolType )
                .size( chooseSymbolSize );

    // NVD3 configuration for force directed graph
    var forceConfig = {
      chart: {
          type: 'forceDirectedGraph',
          height: 300,
          width: 300,
          color: getColour,
          symbol: customSymbol,
          nodeExtras: processNode,
          curveLinks:  true,
          useArrows: true,
          tooltip: { contentGenerator: customTooltipContent }
      }
    };

    // NVD3 configuration for scatter plot
    var scatterGraph = {
      chart: {
          type: "scatterChart",
          height: 500,
          width: 1000,
          color: [ "#1f77b4" ],
          duration: 350,
          zoom: {
            enabled: true,
            scaleExtent: [ 1, 10 ],
            useFixedDomain: false,
            useNiceScale: false,
            horizontalOff: false,
            verticalOff: false,
            unzoomEventType: "dblclick.zoom"
          },
          tooltip: { enabled: false },
          showLabels: false,
          xAxis: {
            showMaxMin: false,
            tickFormat: function() { return ''; }
          },
          yAxis: {
            showMaxMin: false,
            tickFormat: function() { return ''; }
          },
          dispatch: {
            renderEnd: postProcess
          }
      }
    };

    function postProcess(e) {
      // Remove old labels
      d3.selectAll(".label").remove();

      d3.selectAll(".nv-scatterChart path")[0].forEach(function(d) {
        var tf = d3.select(d).attr("transform")
        var t = d3.transform(tf).translate;
        t[0] = t[0] + 10;  //moving the translate x by 10 pixel.
        var d_data = d3.select(d).data();

        if(d_data[0][0]) { // Make sure we can read an object
          var word = d_data[0][0].word;
          d3.select(d.parentNode)
            .append("text")
            .attr("class", "label")
            .text(word)
            .attr("transform", "translate("+t[0]+","+t[1]+")");
        }
      });
    }

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
      // Nodes have: {'name': 'str', 'type': 'seed', 'count': N, year: XXXX},
      addTextLabels(node);
      setSize(node);
      angular.forEach(forceGraphHooks, function(hook) {
        hook(node);
      });
    }

    function addTextLabels(node) {
      node.append("text")
        .attr("dx", 12)
        .attr("dy", ".35em")
        .text(function(d) { return d.name; })
        .style("font-weight", function(d) { return d.type=="seed"?"bold":""; });
    }

    function setSize(node) {
      node.select('circle')
        .attr('r', function(d) { return 5 + 2 * (d.count); });
    }

    function chooseSymbolType(d) {
      if (d.type=="seed") {
        return "triangle-up";
      } else if(d.type=="word") {
        return "circle";
      } else {
        return "diamond";
      }
    }

    function chooseSymbolSize(d) {
      return 50 * Math.log2(2 + d.count);
    }

    function customTooltipContent(d) {
      var showContent = [ 'type', 'count', 'weight' ];

      var html = '<table>';
      html += '<thead><tr><td colspan="2"><strong class="x-value">' + d['name'] + '</strong></td></tr></thead>';
      html += '<tbody>';

      angular.forEach(showContent, function(key) {
        html += '<tr>';
        html += '<td class="key">' + key + '</td>';
        html += '<td class="value">' + d[key] + '</td>';
        html += '</tr>';
      });

      html += '</tbody>';
      html += '</table>';
      return html;
    }

    function addForceGraphHook(callback) {
      forceGraphHooks.push(callback);
    }

    function getConfig(graphName) {
      if(graphName === 'streamGraph') {
        return streamConfig;
      } else if(graphName === 'forceGraph'){
        return forceConfig;
      } else if(graphName === 'scatterGraph'){
        return scatterGraph;
      }
    }
  }
})();
