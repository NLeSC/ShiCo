(function() {
  'use strict';

  angular
    .module('shico')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log) {
    $log.debug('runBlock end');
  }

})();
