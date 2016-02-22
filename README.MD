[![Build Status](https://travis-ci.org/c-martinez/ShiCo.svg?branch=master)](https://travis-ci.org/c-martinez/ShiCo)

# ShiCo package

More documentation will follow

## Launching server

To launch the server run:
```
# python shico/server.py -f "word2vecModels/195?_????.w2v"
```

*Note:* loading the word2vec models takes some time and may consume a large amount of memory.

Then you can access trace a concept by connecting to the server using curl (or your web browser). Examples:

```
http://localhost:5000/track/oorlog
http://localhost:5000/track/oorlog?startKey=1952_1961
http://localhost:5000/track/oorlog?startKey=1952_1961&maxTerms=5
http://localhost:5000/track/oorlog?startKey=1952_1961&maxTerms=5&forwards=
http://localhost:5000/track/nederland?maxTerms=5&sumDistances=true
http://localhost:5000/track/nederland?maxTerms=5&sumDistances=
http://localhost:5000/track/oorlog,oorlogse
```

## Web app 

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


## Unit testing
To run Python unit tests, run:
```
$ nosetests
```
