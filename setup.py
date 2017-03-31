# -*- coding: utf-8 -*-

from setuptools import setup
from octopusEngine.simpleBitcoinMachine import __version__
import os
import io

HERE = os.path.abspath(os.path.dirname(__file__))

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

setup(
    name='simpleBitcoinMachine',
    version=__version__,
    platforms=['OS Independent'],
    description='Light, portable, easy to operate – cashier that allows you to accept payments in Bitcoin (and possibly other cryptocurrencies).',
    long_description=read('README.md'),
    keywords='bitcoin terminal',
    url='https://github.com/octopusengine/simpleBitcoinMachine',
    author='Honza S. Copak',
    author_email='honza.copak@gmail.com',
    license='',
    maintainer='Honza S. Copak',
    maintainer_email='honza.copak@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Other Environment',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Topic :: Office/Business :: Financial',
    ],
    packages=['octopusEngine.simpleBitcoinMachine'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "blockr-python==0.1.0"
    ],
    scripts=[
        'bin/simplebtc',
        'bin/simplebtc_emulator'
    ],
    dependency_links=[
        "git+https://github.com/BrnoPCmaniak/blockr-python.git#egg=blockr-python-0.1.0"
    ]
)
