(function() {
  'use strict';

  angular
    .module('shico', [
      'ngResource',
      'ngAnimate',
      'ui.bootstrap',
      'toastr',
      'nvd3',
      'rzModule',
      'cgBusy',
      'ngSanitize',
      'ngCsv',
      'hc.marked'
    ]);

  nv.utils.symbolMap.set('thin-x', function(size) {
    size = Math.sqrt(size);
    return 'M' + (-size/2) + ',' + (-size/2) +
            'l' + size + ',' + size +
            'm0,' + -(size) +
            'l' + (-size) + ',' + size;
  });
})();
