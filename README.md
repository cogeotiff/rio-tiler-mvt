# rio-tiler-mvt

[![Packaging status](https://badge.fury.io/py/rio-tiler-mvt.svg)](https://badge.fury.io/py/rio-tiler-mvt)
[![CircleCI](https://circleci.com/gh/cogeotiff/rio-tiler-mvt.svg?style=svg)](https://codecov.io/gh/cogeotiff/rio-tiler-mvt)
[![codecov](https://codecov.io/gh/cogeotiff/rio-tiler-mvt/branch/master/graph/badge.svg)](https://circleci.com/gh/cogeotiff/rio-tiler-mvt)


A rio-tiler plugin to translate tile array to MVT (using python-vtzero)

![](https://user-images.githubusercontent.com/10407788/57476379-72cf6000-7264-11e9-979d-bf9f486518c2.png)

More on [COG Talk](https://medium.com/devseed/search?q=cog%20talk) blog posts

## Install

### Requirements

rio-tiler-mvt use [python-vtzero](https://github.com/tilery/python-vtzero) wrapper to encode point and polygons to MVT. Because VTZERO is a C++ library, python-vtzero is written in Cython, thus cython~=0.28 is required to compile this library.

```bash
$ pip install cython~=0.28 # see https://github.com/tilery/python-vtzero#requirements

$ pip install rio-tiler-mvt
```
Or 
```bash
$ git clone http://github.com/cogeotiff/rio-tiler-mvt
$ cd rio-tiler-mvt
$ pip install -e .
```

## Rio-tiler + Mapbox Vector tiles

### API

`mvt.encoder(data, mask, band_names=[], layer_name="my_layer", feature_type="point")`

Inputs:
- data : raster tile data to encode
- mask : mask data
- band_names : Raster band's names
- layer_name : Layer name
- feature_type : Feature type (point or polygon)

Returns:
- mvt : Mapbox Vector Tile encoded data.


## Contribution & Development

Issues and pull requests are more than welcome.

**dev install**

```bash
$ git clone https://github.com/cogeotiff/rio-tiler-mvt.git
$ cd rio-tiler-mvt
$ pip install -e .[dev]
```

**Python3.6 only**

This repo is set to use `pre-commit` to run *flake8*, *pydocstring* and *black* ("uncompromising Python code formatter") when commiting new code.

```bash
$ pre-commit install
```


## Implementations
[cogeo-mosaic](http://github.com/developmentseed/cogeo-mosaic.git)

[satellite-3d](http://github.com/developmentseed/satellite-3d.git)