# rio-tiler-mvt

<p align="center">
  <img src="https://user-images.githubusercontent.com/10407788/57476379-72cf6000-7264-11e9-979d-bf9f486518c2.png" style="max-width: 800px;" alt="rio-tiler"></a>
</p>
<p align="center">
  <em>A rio-tiler plugin to translate tile array to MVT (using python-vtzero).</em>
</p>
<p align="center">
  <a href="https://github.com/cogeotiff/rio-tiler-mvt/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/cogeotiff/rio-tiler-mvt/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://codecov.io/gh/cogeotiff/rio-tiler-mvt" target="_blank">
      <img src="https://codecov.io/gh/cogeotiff/rio-tiler-mvt/branch/master/graph/badge.svg" alt="Coverage">
  </a>
  <a href="https://pypi.org/project/rio-tiler-mvt" target="_blank">
      <img src="https://img.shields.io/pypi/v/rio-tiler-mvt?color=%2334D058&label=pypi%20package" alt="Package version">
  </a>
  <a href="https://github.com/cogeotiff/rio-tiler-mvt/blob/master/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/cogeotiff/rio-tiler-mvt.svg" alt="Downloads">
  </a>
</p>


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

#### **pixel_encoder**

    pixels_encoder(
        data: numpy.ndarray,
        mask: numpy.ndarray,
        band_names: list = [],
        layer_name: str = "my_layer",
        feature_type: str = "point"
    )

Inputs:
- data: raster tile data to encode
- mask: mask data
- band_names: Raster band's names
- layer_name: Layer name
- feature_type: Feature type (point or polygon)

Returns:
- mvt : Mapbox Vector Tile encoded data.

Examples:

```python
from rio_tiler.io import COGReader
from rio_tiler_mvt import pixels_encoder

with COGReader("fixtures/test.tif") as cog
    img = cog.tile(72, 63, 7, resampling_method="nearest")
    mvt = pixels_encoder(img.data, img.mask, layer_name="test", feature_type="point")
```

#### **shapes_encoder**

    shapes_encoder(
        data: numpy.ndarray,  # 1D array (height, width)
        mask: numpy.ndarray,
        layer_name: str = "my_layer",
        colormap: dict = {},
        class_names: dict = {}
    )

Inputs:
- data: raster tile data to encode
- mask: mask data
- layer_name: Layer name
- colormap: GDAL colormap. If provided a `color` value will be added to the feature properties
- class_names: Dictionary mapping pixel value with class names. If provided a `name` value will be added to the feature properties.

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

**Python3.7 only**

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
$ pre-commit install
```

[satellite-3d](http://github.com/developmentseed/satellite-3d.git)
