import numpy 

from vtzero.tile import Tile, Layer, Point, Polygon

cimport numpy

cpdef bytes encoder(
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