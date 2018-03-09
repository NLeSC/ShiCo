# Deploying ShiCo
If you want to run your own instance of ShiCo, there are a few things you will need:

 - A set of word2vec models which your ShiCo instance will use.
 - Run the python back end on your a server (you will need a server with enough memory to hold your word2vec models).
 - Run a web server to serve the front end to the browser.

## Word2vec models

You are welcome to use our [existing w2v models](http://doi.org/10.5281/zenodo.1189328). If you do, please contact us for more details on how the models were build and to know how to cite our work. You can also [create your own](./buildingModels.md) models, based on your own corpus.

## Launching the back end

Once you have downloaded the code (or clone this repo), and install all Python requirements (contained in *requirements.txt*), you can launch the flask server as follows:
```
$ python shico/server/app.py -f "word2vecModels/????_????.w2v"
```

*Note:* loading the word2vec models takes some time and may consume a large amount of memory.

You can check that the server is up and running by connecting to the server using curl (or your web browser):
```
http://localhost:5000/load-settings
```

Alternatively you use [Gunicorn](http://gunicorn.org/), by setting your configuration on *shico/server/config.py* and then running:

```
$ gunicorn --bind 0.0.0.0:8000 --timeout 1200 shico.server.wsgi:app
```

## Launching the front end

The necessary files for serving the front end are located in the *webapp* folder. You will need to edit your configuration file (*webapp/srs/config.json*) to tell the front end where your back end is running. For example, if your backend is running on *localhost* port 5000 as in the example above, you would set your configuration file as follows:

```
{
  "baseURL": "http://localhost:5000"
}
```

If you are familiar with the Javascript world, you can use the *gulp* tasks provided. You can serve your front end as follows (from the *webapp* folder):
```
$ gulp serve
```

You can build a deployable version (minified, uglified, etc) as follows:
```
$ gulp build
```
This will build a deployable version on the *webapp/dist* folder.

## Pre-build deployable version

If you are not familiar with the Javascript world (or just don't feel like building your own deployable version), the *demo* branch of this repository contains a pre-build version of the front end. You can checkout (or download) that branch, and then you are ready to go.

## Serve with your favorite web server

Once you have a *webapp/dist* folder (whether downloaded or self built) you can serve the content of it using your favorite web server. For example, you could use Python SimpleHTTPServer as follows (from the *webapp/dist* folder):
```
$ python -m SimpleHTTPServer
```

## Cleaning functions
In some cases, resulting vocabularies may contain words which we would like to filter. ShiCo offers the possibility of using a *cleaning* function, for filtering vocabularies after they have been generated. To use this option, it is necessary to indicate the name of the cleaning function when starting the ShiCo server. A sample cleaning function is provided (*shico.extras.cleanTermList*). You can use this function as follows:
```
$ python shico/server/app.py -c "shico.extras.cleanTermList"
```

If you are using gunicorn, in your *config.py*, you can set `cleaningFunctionStr` to the name of your cleaning function, for instance:

```
cleaningFunctionStr = "shico.extras.cleanTermList"
```

## Speeding up ShiCo

Current implementation of ShiCo relies on gensim word2vec model `most_similar` function, which in turn requires the calculation of the dot product between two large matrices, via `numpy.dot` function. For this reason, ShiCo greatly benefits from using libraries which accelerate matrix multiplications, such as OpenBLAS. ShiCo has been tested using [Numpy with OpenBLAS](https://hunseblog.wordpress.com/2014/09/15/installing-numpy-and-openblas/), producing a significant increase in speed.
