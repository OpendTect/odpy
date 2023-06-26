[![License](https://img.shields.io/github/license/analysiscenter/batchflow.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Python](https://img.shields.io/badge/python-3.7-blue.svg)](https://python.org)
[![Numpy](https://img.shields.io/badge/numpy-1.19-green.svg)](https://numpy.org)
[![h5py](https://img.shields.io/badge/h5py-2.10-red.svg)](https://docs.h5py.org)

# odpy

`odpy` is a framework for research and deployment that allows for basic interactions with the OpendTect software and database

* Locates/set the path to the OpendTect installation
* Locates/set the path to the OpendTect database
* Complements h5py for an easier manipulation of hdf5 attributes
* Easy loading of well logs from the OpendTect database


## Installation

With [pipenv](https://docs.pipenv.org/):

    pipenv install git+https://github.com/OpendTect/odpy.git#egg=odpy

With [pip](https://pip.pypa.io/en/stable/):

    pip3 install git+https://github.com/OpendTect/odpy.git

After that just import `odpy`:
```python
import odpy
```

To get the developer version, run
```
git clone --recursive https://github.com/OpendTect/odpy.git
```

## Documentation

* [odpy API reference](https://doc.opendtect.org/7.0.0/doc/odpy/index.html)

## Citing odpy

Please cite `odpy` in your publications if it helps your research.

    Huck A., and Ibrahim O. odpy library for OpendTect access. 2019.

```
@misc{odpy_2019,
  author       = {A. Huck and O. Ibrahim},
  title        = {odpy library for OpendTect access},
  year         = 2019
}
```
