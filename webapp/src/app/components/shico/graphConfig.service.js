(function() {
  'use strict';

  angular
      .module('shico')
      .service('GraphConfigService', GraphConfigService);

  function GraphConfigService($log) {
    // TODO: streamConfig could be loaded from JSON ?

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
          }
      }
    };

    var service = {
      getConfig: getConfig
    };
    return service;

    // TODO: remove these functions
    function getX(d){ return d[0]; }
    function getY(d){ return d[1]; }
    function tickYear(d) { return d + '_'; }

    function getConfig(graphName) {
      if(graphName === 'streamGraph') {
        return streamConfig;
      } else {
        return {};
      }
    }
  }
})();
