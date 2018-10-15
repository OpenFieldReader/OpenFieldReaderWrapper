# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='openfieldreaderwrapper',
    version='1.0.0',
    description='A wrapper around the openfieldreader command line tool to automatically detect paper-based form fields.',
    url='https://github.com/OpenFieldReader/OpenFieldReader',
    author='Philip Doxakis',
    author_email='philip@doxakis.com',
    license='MIT',
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='icr',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=[
        'opencv-python'
    ]
)