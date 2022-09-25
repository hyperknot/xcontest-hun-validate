from setuptools import setup

requirements = [
    'ipython',
    'click',
    'pygeos',
    'geojson',
]

setup(name='xcontest_hun_validate', python_requires='>=3.9', install_requires=requirements)
