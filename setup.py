from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='buoyant',

    version='0.2.2',

    description="Wrapper for the NOAA National Data Buoy Center",

    long_description=read_md('readme.md'),

    url='https://github.com/fitnr/buoyant',

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    license='GPL',

    packages=['buoyant'],

    install_requires=[
        'lxml>=3.3',
        'requests>=2.4.1'
    ],

    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Scientific/Engineering :: Atmospheric Science',
        'Intended Audience :: Science/Research',
    ],
)
