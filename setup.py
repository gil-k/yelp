from setuptools import find_packages
from setuptools import setup

setup(
    name='Yelp Photos',

    version='1.43',

    description='Yelp search results displays user photos',

    url='',

    author='KD Kwak',
    # author_email='kd@atitan.net',

    # classifiers=[
    #     'License :: OSI Approved :: MIT License',
    #     'Programming Language :: Python :: 2.7'
    # ],

    # license='MIT',

    # keywords='yelp', 'photos', 'visual'

    packages=find_packages(exclude=('venv*',)),

    install_requires=[
        'httplib2',
        'oauth2',
        'six',
        'requests',
        'grequests',
        'Flask'
    ],
)
