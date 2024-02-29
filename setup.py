""" odpy contains generic python tools for OpendTect. """

from setuptools import setup, find_packages
import re

with open('odpy/__init__.py', 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

setup(
    name='odpy',
    packages=find_packages(exclude=[]),
    version=version,
    url='https://github.com/OpendTect/odpy',
    license='Apache 2.0',
    author='dGB Earth Sciences',
    author_email='info@dgbes.com',
    description='Generic tools for access to OpendTect sofware and database',
    long_description='',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'h5py>=2.10.0',
        'numba>=0.53.1',
        'numpy>=1.19.2',
        'psutil>=5.7.0',
    ],
    extras_require={
        'humanfriendly': ['humanfriendly>=9.2.0'],
        'matplotlib': ['matplotlib>=3.0.0'],
        'odbind': ['odbind>=1.0.0'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    ],
)
