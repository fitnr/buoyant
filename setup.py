from setuptools import setup

setup(
    name='data_buoy',

    version='0.1.0',

    description='buoy data from the NOAA',

    long_description="Wrapper for NOAA National Data Buoy Center",

    url='',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='All rights reserved',

    packages=['data_buoy'],

    install_requires=[
        'lxml>=3.3',
        'requests>=2.4.1'
    ],

)
