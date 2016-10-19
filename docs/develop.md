# What should you do if you want to modify ShiCo?

Be brave! And get in touch if you need help. Pull requests are very welcome.

## Backend

Written in Python.

### Unit testing
If you modify ShiCo back end, make sure to write your unit tests for your code.

To run Python unit tests, run:
```
$ nosetests
```

## Web app

Written in Javascript (Angular).

### Adding hooks

You can add your own custom behaviour to the force directed graphs like this:
```
(function() {
 'use strict';

 angular
   .module('shico')
   .run(runBlock);

 function runBlock(GraphConfigService) {
   GraphConfigService.addForceGraphHook(function(node) {
     node.select('circle').attr('r', function(d) {
       return d.name.length;
     });
   });
 }
})();

```

This snippet modifies the size of the force directed graph nodes, and makes them dependent on the length of the name in the node's data.

## Making a release on GitHub
 - Merge changes on branch `demo`
 - Run `gulp build`
 - Make github release
