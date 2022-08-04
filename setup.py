from setuptools import setup

requirements = [
    'ipython',
    'click',
    'pygeos',
    'geojson',
    # 'pyproj',
    'psycopg2-binary',
    'vincenty',
]

setup(name='legter_check', python_requires='>=3.9', install_requires=requirements)
