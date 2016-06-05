# https://packaging.python.org/en/latest/distributing.html
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open
from os import path
import easy_dict

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

classifiers = '''
Intended Audience :: Developers
Intended Audience :: Education
Intended Audience :: Financial and Insurance Industry
Intended Audience :: Information Technology
Intended Audience :: Other Audience
Intended Audience :: Science/Research
License :: OSI Approved :: MIT License
Programming Language :: Python :: 3.3
Programming Language :: Python :: 3.4
Programming Language :: Python :: 3.5
'''

setup(
    name='easy_dict',
    version=easy_dict.__version__,
    description='Easier way of accessing & assigning information in a nested dictionary.',
    long_description=long_description,
    url='https://github.com/cahoy/NestedDictionary',
    author='Cahyo Primawidodo',
    author_email='cahyo.p@gmail.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[x for x in classifiers.split('\n') if x],
    keywords='easy simple nested flat default dictionary',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        '': ['README.md']
    },
)