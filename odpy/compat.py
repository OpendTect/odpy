"""Compatibility helpers for odpy

Copyright (C) dGB Beheer B.V.; (LICENSE) http://opendtect.org/OpendTect_license.txt

Module Summary
###############

Shims for the library-version boundaries odpy span (numpy 1.x/2.x,
hdf5 1.14/2.x, torch < 2.6 and >= 2.6). Each helper says which boundary it
covers so it can be removed once the older version is retired.
"""

import importlib
import importlib.util
import inspect

import numpy as np


def optional_import( name ):
  """ Imports a module that may be absent

  Parameters:
    * name (str): module name

  Returns:
    * module: the imported module, or None when it is not installed
  """

  try:
    return importlib.import_module( name )
  except ImportError:
    return None


def has_module( name ):
  """ Checks whether a module can be imported, without importing it

  Parameters:
    * name (str): module name

  Returns:
    * bool: True if the module is available
  """

  try:
    return importlib.util.find_spec( name ) is not None
  except (ImportError, ValueError):
    return False


class MissingModule:
  """ Placeholder for an optional module that is not installed

  Any attribute access or call raises ImportError naming the package.
  """

  def __init__( self, name, purpose=None ):
    self._name = name
    self._purpose = purpose

  def _fail( self ):
    msg = "'" + self._name + "' is not installed"
    if self._purpose:
      msg += ', which is required for ' + self._purpose
    raise ImportError( msg )

  def __getattr__( self, item ):
    self._fail()

  def __call__( self, *args, **kwargs ):
    self._fail()

  def __bool__( self ):
    return False


def optional_module( name, purpose=None ):
  """ As optional_import, but returns a MissingModule instead of None

  Parameters:
    * name (str): module name
    * purpose (str, optional): used in the ImportError raised on first use

  Returns:
    * module or MissingModule
  """

  mod = optional_import( name )
  if mod is None:
    return MissingModule( name, purpose )
  return mod


# numpy 2.0 removed np.chararray; np.char has the same functions on both.
_NP_CHAR = np.char if hasattr( np, 'char' ) else getattr( np, 'chararray' )


def char_encode( value ):
  """ Encodes a string to a fixed-length numpy bytes scalar (dtype '|S<n>')

  Parameters:
    * value (str): text to encode

  Returns:
    * ndarray: 0-d array of dtype '|S<n>'
  """

  return _NP_CHAR.encode( value )


def char_startswith( arr, prefix ):
  """ Elementwise str.startswith over an array of strings

  Parameters:
    * arr (list, ndarray): strings to test
    * prefix (str): prefix to test for

  Returns:
    * ndarray: boolean array
  """

  return _NP_CHAR.startswith( arr, prefix )


_Version = None
try:
  from packaging.version import Version as _Version
except ImportError:
  pass


def _versiontuple( ver ):
  parts = []
  for chunk in str( ver ).split( '.' ):
    digits = ''
    for ch in chunk:
      if not ch.isdigit():
        break
      digits += ch
    parts.append( int(digits) if digits else 0 )
  return tuple( parts )


def version_at_least( actual, minimum ):
  """ Compares two version strings numerically

  Parameters:
    * actual (str): the installed version, e.g. sklearn.__version__
    * minimum (str): the lowest version that qualifies

  Returns:
    * bool: True when actual >= minimum
  """

  if _Version is not None:
    return _Version( actual ) >= _Version( minimum )
  return _versiontuple( actual ) >= _versiontuple( minimum )


def torch_supports_weights_only( torch_module ):
  """ Checks whether torch.load accepts the weights_only argument (torch >= 1.13)

  Parameters:
    * torch_module (module): the imported torch module

  Returns:
    * bool
  """

  try:
    return 'weights_only' in inspect.signature( torch_module.load ).parameters
  except (TypeError, ValueError):
    return False


def ensure_h5py_state():
  """ Re-creates h5py's cached default property lists when they are invalid

  Another HDF5 user in the same process (OpendTect's ODHDF5) can invalidate
  them, after which create_group/create_dataset fail with
  KeyError("Property object doesn't exist"). Uses private h5py API, so every
  step is guarded and never raises.
  """

  try:
    from h5py._hl import base
  except Exception:
    return

  for nm, factory in (('dlcpl','default_lcpl'), ('dlapl','default_lapl')):
    try:
      cur = getattr( base, nm, None )
      if cur is not None and cur.valid:
        continue
      mk = getattr( base, factory, None )
      if mk is not None:
        setattr( base, nm, mk() )
    except Exception:
      pass

  # Also re-create on use, as they can be invalidated again at any time.
  try:
    if getattr( base, '_od_plist_guard', False ):
      return
    cls = getattr( base, 'CommonStateObject', None )
    if cls is None:
      return

    def _mkprop( nm, factory ):
      def _get( self ):
        cur = getattr( base, nm )
        try:
          ok = cur.valid
        except Exception:
          ok = False
        if not ok:
          setattr( base, nm, getattr(base, factory)() )
          cur = getattr( base, nm )
        return cur
      return property( _get )

    if hasattr( cls, '_lcpl' ) and hasattr( base, 'default_lcpl' ):
      cls._lcpl = _mkprop( 'dlcpl', 'default_lcpl' )
    if hasattr( cls, '_lapl' ) and hasattr( base, 'default_lapl' ):
      cls._lapl = _mkprop( 'dlapl', 'default_lapl' )
    base._od_plist_guard = True
  except Exception:
    pass


def h5py_libver( low='v110', high='v114' ):
  """ Builds a libver bound pair for h5py.File, checked against the installed h5py

  Parameters:
    * low (str): lowest format version the file may use
    * high (str): highest format version the file may use

  Returns:
    * tuple: (low, high), with 'earliest'/'latest' substituted for unknown names
  """

  try:
    from h5py._hl.files import libver_dict
  except Exception:
    return ( low, 'latest' )
  if low not in libver_dict:
    low = 'earliest'
  if high not in libver_dict:
    high = 'latest'
  return ( low, high )
