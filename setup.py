from setuptools import find_packages
from setuptools import setup

setup(
    name='yelp',

    version='1.2',

    description='Yelp search results displayed with gallery of user photos of businesses',

    url='',

    author='K.D. Kwak',
    author_email='gil@atitan.net',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
    ],

    license='MIT',

    keywords='yelp',

    packages=find_packages(exclude=('BASELINE*',)),

    install_requires=[
        'httplib2',
        'oauth2',
        'six',
    ],
)
