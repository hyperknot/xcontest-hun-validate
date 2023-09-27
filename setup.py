from setuptools import setup

requirements = [
    'ipython',
    'click',
    'pygeos',
    'geojson',
    'requests',
]

setup(
    name='xcontest_hun_validate',
    python_requires='>=3.9',
    install_requires=requirements,
    packages=['lib'],
)
