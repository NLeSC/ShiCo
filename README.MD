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
```

## Unit testing
To run Python unit tests, run:
```
$ nosetests
```
