(function() {
  'use strict';

  angular
    .module('shico')
    .run(runBlock);

  /** @ngInject */
  function runBlock($log, SettingsService) {
    $log.debug('runBlock end');
    SettingsService.doLoad();
  }

})();
