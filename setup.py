from setuptools import setup

def read_md(f):
    try:
        try:
            from pypandoc import convert
            return convert(f, 'rst')

        except ImportError:
            print("pypandoc not found, could not convert Markdown to RST")
            return open(f, 'r').read()

    except (IOError, RuntimeError):
        print("Could not read readme.md")
        return ''

setup(
    name='buoyant',

    version='0.2.3',

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
