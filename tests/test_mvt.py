"""tests rio_tiler_mvt."""

import os

import pytest
import vector_tile_base

from rio_tiler.io import COGReader
from rio_tiler_mvt import pixels_encoder, shapes_encoder
from rio_tiler_mvt.mvt import encoder


def test_pixels_encoder():
    """Test MVT encoder."""
    asset = os.path.join(os.path.dirname(__file__), "fixtures", "test.tif")
    x = 72
    y = 63
    z = 7

    with COGReader(asset) as cog:
        tile, mask = cog.tile(x, y, z, resampling_method="nearest")

    # test with default
    vt = pixels_encoder(tile, mask)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    assert len(layer.features) == 75
    feat = layer.features[0]
    assert feat.type == "point"
    props = feat.attributes
    assert len(props) == 1
    assert props["band1"] == "21.08714485168457"

    # Test polygon
    vt = pixels_encoder(tile, mask, feature_type="polygon")
    mvt = vector_tile_base.VectorTile(vt)
    layer = mvt.layers[0]
    feat = layer.features[0]
    assert feat.type == "polygon"
    props = feat.attributes
    assert props["band1"] == "21.08714485168457"

    # Test band name
    vt = pixels_encoder(tile, mask, band_names=["pop"])
    mvt = vector_tile_base.VectorTile(vt)
    props = mvt.layers[0].features[0].attributes
    assert props["pop"] == "21.08714485168457"

    # Test layer name
    vt = pixels_encoder(tile, mask, layer_name="facebook")
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "facebook"

    with pytest.warns(DeprecationWarning):
        vt = encoder(tile, mask)
        mvt = vector_tile_base.VectorTile(vt)
        assert len(mvt.layers) == 1

    # Test bad feature type
    with pytest.raises(Exception):
        pixels_encoder(tile, mask, feature_type="somethingelse")


def test_shapes_encoder():
    """Test MVT encoder."""
    asset = os.path.join(os.path.dirname(__file__), "fixtures", "cog_classes.tif")
    x, y, z = 814, 1750, 12
    with COGReader(asset) as cog:
        tile, mask = cog.tile(x, y, z, resampling_method="nearest", tilesize=256)

    # test with default
    vt = shapes_encoder(tile[0], mask)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    with COGReader(asset) as cog:
        tile, mask = cog.tile(x, y, z, resampling_method="nearest", tilesize=4096)
        colormap = cog.colormap
        classes = {0: "none", 1: "grass", 2: "urban", 18: "something"}

    # test with default
    vt = shapes_encoder(tile[0], mask)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    feat = layer.features[0]
    assert feat.type == "polygon"
    props = feat.attributes
    assert len(props) == 1
    assert props["value"]

    vt = shapes_encoder(tile[0], mask, colormap=colormap, class_names=classes)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    feat = layer.features[0]
    assert feat.type == "polygon"

    props = feat.attributes
    assert len(props) == 2
    assert props["color"] == "#4c70a3"
    assert props["name"] == "something"
