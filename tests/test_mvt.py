"""tests ard_tiler.mosaic."""

import os

import pytest

from rio_tiler.main import tile as cogTiler
from rio_tiler_mvt.mvt import encoder

import vector_tile_base

asset = os.path.join(os.path.dirname(__file__), "fixtures", "test.tif")
x = 72
y = 63
z = 7

tile, mask = cogTiler(asset, x, y, z, resampling_method="nearest")


def test_mvt_encoder():
    """Test MVT encoder."""
    # test with default
    vt = encoder(tile, mask)
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "my_layer"
    assert layer.extent == 4096
    assert layer.version == 2

    assert len(layer.features) == 75
    feat = layer.features[0]
    assert feat.type == "point"
    props = feat.properties
    assert len(props) == 1
    assert props["band1"] == "21.08714485168457"

    # Test polygon
    vt = encoder(tile, mask, feature_type="polygon")
    mvt = vector_tile_base.VectorTile(vt)
    layer = mvt.layers[0]
    feat = layer.features[0]
    assert feat.type == "polygon"
    props = feat.properties
    assert props["band1"] == "21.08714485168457"

    # Test band name
    vt = encoder(tile, mask, band_names=["pop"])
    mvt = vector_tile_base.VectorTile(vt)
    props = mvt.layers[0].features[0].properties
    assert props["pop"] == "21.08714485168457"

    # Test layer name
    vt = encoder(tile, mask, layer_name="facebook")
    mvt = vector_tile_base.VectorTile(vt)
    assert len(mvt.layers) == 1
    layer = mvt.layers[0]
    assert layer.name == "facebook"

    # Test bad feature type
    with pytest.raises(Exception):
        encoder(tile, mask, feature_type="somethingelse")
