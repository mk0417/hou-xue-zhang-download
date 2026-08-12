from setuptools import setup, find_packages

setup(
    name='hxz_download',
    version='0.0.1',
    author='Peng Li',
    license='GPLv2',
    packages=find_packages(),
    install_requires=[
        'polars',
        'pandas',
        'beautifulsoup4',
        'requests'
    ],
)
