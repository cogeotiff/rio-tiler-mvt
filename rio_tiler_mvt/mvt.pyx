
import warnings

import numpy
cimport numpy

from vtzero.tile import Tile, Layer, Point, Polygon

from rasterio._features import _shapes
from rasterio.rio.helpers import coords
from rasterio.transform import IDENTITY
from shapely import geometry


cpdef bytes pixels_encoder(
    data,
    mask,
    list band_names = [],
    str layer_name = "my_layer",
    str feature_type = "point",
):
    cdef int sc = 4096 // data.shape[1]
    cdef tuple indexes = numpy.where(mask)

    cdef tuple idx
    cdef int x, y

    if not band_names:
        band_names = [
          f"band{ix}" for ix in range(1, data.shape[0] + 1)
        ]

    mvt = Tile()
    mvt_layer = Layer(mvt, layer_name.encode())
    for idx in zip(indexes[1], indexes[0]):
        x, y = idx
        x *= sc
        y *= sc

        if feature_type == 'point':
            feature = Point(mvt_layer)
            feature.add_point(x + sc / 2, y - sc / 2)

        elif feature_type == 'polygon':
            feature = Polygon(mvt_layer)
            feature.add_ring(5)
            feature.set_point(x, y)
            feature.set_point(x + sc, y)
            feature.set_point(x + sc, y - sc)
            feature.set_point(x, y - sc)
            feature.set_point(x, y)
        else:
            raise Exception(f"Invalid geometry type: {feature_type}")

        # TODO: fix https://github.com/tilery/python-vtzero/issues/3
        for bidx in range(data.shape[0]):
            feature.add_property(
                band_names[bidx].encode(),
                str(data[bidx, idx[1], idx[0]]).encode()
            )
        feature.commit()

    return mvt.serialize()


cpdef bytes encoder(
    data,
    mask,
    list band_names = [],
    str layer_name = "my_layer",
    str feature_type = "point",
):
    """Compatibility with previous version."""
    warnings.warn(
        "'mvt.encoder' function will be deprecated in next version, please use 'mvt.pixels_encoder'",
        DeprecationWarning,
    )
    return pixels_encoder(data, mask, band_names, layer_name, feature_type)


cpdef bytes shapes_encoder(
    data,
    mask,
    str layer_name = "my_layer",
    dict colormap = {},
    dict class_names = {},
):
    """Encode polygon extracted from GDAL polygonize.

    Args:
        data (numpy.ndarray): image data.
        mask (numpy.ndarray): mask array.
        layer_name (str): MVT layer name.
        colormap (dict): GDAL colormap. If provided a `color` value will be added
            to the feature properties.
        class_names (dict): Dictionary mapping pixel value with class names. If provided
            a `name` value will be added to the feature properties.

    Returns:
        bytes: Mapbox Vector Tile.

    """
    cdef float x, y
    cdef int r, g, b

    mvt = Tile()
    mvt_layer = Layer(mvt, layer_name.encode())

    # scaling factor
    cdef int sc = 4096 // max(data.shape)

    # Iterate through shapes and values
    for (p, v) in _shapes(data, mask, connectivity=4, transform=IDENTITY.scale(sc)):
        # make sure v is the same datatype as the input data
        v = data.dtype.type(v)
        feature = Polygon(mvt_layer)
        feature.set_id(v)

        polygon = geometry.shape(p)
        # Simple GEOS Validation
        if not polygon.is_valid:
            # If the polygon is not valid we use a little trick
            polygon = polygon.buffer(0)

        # add exterior ring
        feature.add_ring(len(polygon.exterior.coords))
        for x, y in polygon.exterior.coords:
            feature.set_point(int(x), int(y))

        # add interior rings
        for polygon_interior in list(polygon.interiors):
            feature.add_ring(len(polygon_interior.coords))
            for x, y in polygon_interior.coords:
                feature.set_point(int(x), int(y))

        if colormap:
            r, g, b, _ = colormap.get(v, (0, 0, 0, 0))
            feature.add_property("color".encode(), '#{:02x}{:02x}{:02x}'.format(r, g, b).encode())

        if class_names:
            feature.add_property("name".encode(), class_names.get(v, "").encode())
        else:
            feature.add_property("value".encode(), str(v).encode())

        feature.commit()

    return mvt.serialize()
