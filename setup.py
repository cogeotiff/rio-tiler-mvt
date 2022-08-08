"""Setup for rio-tiler-mvt."""

import numpy
from Cython.Build import cythonize
from setuptools import find_packages, setup
from setuptools.extension import Extension

with open("README.md") as f:
    long_description = f.read()

inst_reqs = ["numpy", "vtzero", "rasterio", "shapely"]

extra_reqs = {
    "test": [
        "vector-tile-base @ git+https://github.com/mapbox/vector-tile-base.git",
        "protobuf==3.20.1",
        "rio-tiler>=2.0",
        "pytest",
        "pytest-cov",
    ],
    "dev": ["pre-commit"],
}

ext_options = {"include_dirs": [numpy.get_include()]}
ext_modules = cythonize(
    [Extension("rio_tiler_mvt.mvt", ["rio_tiler_mvt/mvt.pyx"], **ext_options)]
)

setup(
    name="rio-tiler-mvt",
    description="""A rio-tiler plugin to encode tile array to MVT""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    keywords="COG MVT mapbox vectortile GIS",
    author="Vincent Sarago",
    author_email="vincent@developmentseed.org",
    url="https://github.com/cogeotiff/rio-tiler-mvt",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    include_package_data=True,
    zip_safe=False,
    install_requires=inst_reqs,
    extras_require=extra_reqs,
    ext_modules=ext_modules,
)
