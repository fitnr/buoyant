from setuptools import setup

setup(
    name='buoyant',

    version='0.2.1',

    description='buoy data from the NOAA',

    long_description="Wrapper for NOAA National Data Buoy Center",

    url='https://github.com/fitnr/buoyant',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='All rights reserved',

    packages=['buoyant'],

    install_requires=[
        'lxml>=3.3',
        'requests>=2.4.1'
    ],

)
