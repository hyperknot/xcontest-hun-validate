from setuptools import setup

requirements = [
    'ipython',
    'click',
    'pygeos',
    'geojson',
    'pyproj',
]

setup(name='legter_check', python_requires='>=3.9', install_requires=requirements)
