"""Common tools for odpy package

Copyright (C) dGB Beheer B.V.; (LICENSE) http://opendtect.org/OpendTect_license.txt
  * AUTHOR : A. Huck
  * DATE   : July 2018

Module Summary
###############

odpy.common is the main important module in odpy. Allows for basic interactions with the OpendTect software and database

KEY methods
-------------

* getODsoftwareDir()

  * gets the root directory of the Opendtect installation

* getODargs()

  * get dict containing information about the Opendtect executable, project database path and current survey name

Example
--------
>>> import odpy.common as odcommon
>>> odcommon.getODSoftwareDir()
    Windows: 'C:\\Program Files\\OpendTect\\2025'
    Linux: '/home/user/OpendTect/2025'
    MacOS: '/Applications/OpendTect/OpendTect 2025.app/Contents'

>>> odcommon.getODArgs()
    {'dtectexec': ['C:\\PROGRA~1\\OPENDT~1\\new\\6683E8~1.0\\bin\\win64\\Release'],
     'dtectdata': ['C:\\Users\\OLAWALE IBRAHIM\\DTECT_DATA'],
     'survey': ['F3_Demo_2020']}

"""

import sys
import os
import platform
import logging
from datetime import datetime
from enum import Enum
import threading

def sTimeUnitString( ismilli=False, abbr=True ):
  """OpendTect-like time stamp

  Parameters:
    * ismilli (bool, optional): Include millisecond (default is False)
    * abbr (bool, optional): Abbreviated (default is True)

  Returns:
    * str: Time stamp string formatted like done by OpendTect

  Examples:
    >>> sTimeUnitString()
    'Mon 20 Apr 2020, 13:59:54'

    >>> sTimeUnitString( True )
    'Mon 20 Apr 2020, 13:59:54.001245'

    >>> sTimeUnitString( True, True )
    'Mon 20 Apr 2020, 13:59:54.001245'

    >>> sTimeUnitString( True, False )
    'Monday 20 April 2020, 13:59:54'

  """

  if abbr:
    fmt = "%a %d %b"
  else:
    fmt = "%A %d %B"
  fmt += " %Y, %X"
  if ismilli:
    fmt += ".%f"
  return datetime.now().strftime(fmt)

try:
  from bokeh.util import logconfig
except ImportError:
  logconfig = None

syslog_logger = logging.getLogger(__name__)
proclog_logger = logging.getLogger('odproclog')

if not syslog_logger.hasHandlers():
  handler = logging.StreamHandler(sys.stdout)
  syslog_logger.setLevel( 'INFO' )
  syslog_logger.addHandler( handler )

if not proclog_logger.hasHandlers():
  handler = logging.StreamHandler(sys.stdout)
  proclog_logger.setLevel( 'DEBUG' )
  proclog_logger.addHandler( handler )

def initLogging(args):
  """odpy Logger initialization

  Parameters:
    * args (dict):
      The members 'logfile' and 'sysout' from the input dictionary are supposed to contain existing filenames which are used
      to setup the module loggers proclog_logger and syslog_logger

  """

  set_log_file( args['logfile'].name, proclog_logger )
  set_log_file( args['sysout'].name, syslog_logger )

def set_log_file( filenm, logger ):
  """Sets log file with the handler based on the filename

  Parameters:
    * filenm (str): log file name
    * logger (object): log object

  Returns:
    Nothing. 
    Removes past handlers if any and sets new log handler type based on file name
  
  """

  for handler in logger.handlers:
    logger.removeHandler( handler )
  if filenm == '<stdout>' or filenm == 'stdout':
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler( handler )
    return
  elif filenm == '<stderr>' or filenm == 'stdout':
    handler = logging.StreamHandler(sys.stderr)
    logger.addHandler( handler )
    return
  if not os.path.isfile(filenm):
    std_msg( 'Log file not found: ', filenm )
    return
  handler = logging.FileHandler(filenm,'a')
  logger.addHandler( handler )
  logger.propagate = False

def get_log_logger():
  """ Returns logger
  
  """
  return proclog_logger

def get_std_logger():
  """ Returns module logger
  
  """
  return syslog_logger

def mergeArgs(a,b=None,c=None,d=None,e=None,f=None):
  """Concatenates input strings and objects if more than one as single string
  
  Parameters:
    * a (object or string): Message to be printed
    * b-f (object or string, optional): Message to be printed

  Returns:
    * str: Concatenated string

  Notes:
    * All objects are formatted to strings using the str() function
    * All outputs are automatically separated by spaces.
  """
  
  msg = str(a)
  if b != None:
    msg = msg+' '+str(b)
  if c != None:
    msg = msg+' '+str(c)
  if d != None:
    msg = msg+' '+str(d)
  if e != None:
    msg = msg+' '+str(e)
  if f != None:
    msg = msg+' '+str(f)
  return msg

def std_msg(a,b=None,c=None,d=None,e=None,f=None):
  """Print to odpy standard logger

  Parameters:
    * a (object or string): Message to be printed
    * b-f (object or string, optional): Message to be printed

  Prints:
    * str: Concatenated string

  Notes:
    * All objects are formatted to strings using the str() function
    * All outputs are automatically separated by spaces.
    * Reserved for standard logging information.

  """

  msg = mergeArgs(a,b,c,d,e,f)
  get_std_logger().info(msg)

def log_msg(a,b=None,c=None,d=None,e=None,f=None):
  """Print to odpy processing logger

  Parameters:
    * a (object or string): Message to be printed
    * b-f (object or string, optional): Message to be printed

  Returns:
    * str: Concatenated string

  Notes:
    * All objects are formatted to strings using the str() function
    * All outputs are automatically separated by spaces.
    * Reserved for processing logging information,
    * i.e. to report progress on a task

  """
  msg = mergeArgs(a,b,c,d,e,f)
  get_log_logger().debug(msg)

def has_file_handlers(logger):
  """To check if a log file has a file handler

  Parameters:
    * logger (object): Logger file object
  
  Returns:
    * bool: True if logger is a file handler logger
  """

  for handler in logger.handlers:
    if isinstance( handler, logging.FileHandler ):
      return True
  return False

def has_stdlog_file():
  """ Checks if module log has a file handler

  Returns
    * bool: True if module log file has a File handler and False if otherwise
  """

  return has_file_handlers( get_std_logger() )

def has_log_file():
  """ Checks if log (odproclog) has a file handler
  
  Returns:
  * bool: True if log file (odproclog) has a File handler and False if otherwise
  """

  return has_file_handlers( get_log_logger() )

def get_handler_stream(logger):
  """ Gets log handler stream
  
  Parameters:
    * logger (object): log file object

  Returns:
      * str: where log info streams to if log handler exist, 
      returns None if handler level is not set
  """
  for handler in logger.handlers:
    if isinstance( handler, logging.StreamHandler ) and handler.level != logging.NOTSET:
      return handler.stream
    elif isinstance( handler, logging.FileHandler ) and handler.level != logging.NOTSET:
      return handler.stream
  return None

def get_handler_filename(logger):
  """Gets logger filename

  Parameters:
    * logger (object): log file object

  Returns:
    * str: Log file name if any, None if not
  
  """
  for handler in logger.handlers:
    if isinstance( handler, logging.FileHandler ):
      return handler.baseFilename
  return None

def get_std_stream():
  """ Gets current module stream handler

  Returns:
    * str: log stream handler name
  
  """

  return get_handler_stream( get_std_logger() )

def get_log_stream():
  """Gets odpy.commom log stream handler

  Returns:
    * str: log stream handler name
  
  """
  
  return get_handler_stream( get_log_logger() )

def get_stdlog_file():
  """ Full log file path for current module

  Returs:
    * str: Path to log file for current module
  """

  return get_handler_filename( get_std_logger() )

def get_log_file():
  """ Full log file path for odpy.common

  Returs:
    * str: Path to log file for odpy.common
  """

  return get_handler_filename( get_log_logger() )

def reset_log_file( keeplines=0 ):
  """Log file reset

  Parameters:
    * keeplines (int, optional): 
      Number of lines from the top of the file to keep (default is 0)

  Empty the log file pointed at by the processing logger,
  for instance before starting a new task.

  """

  if not has_log_file():
    return
  logfnm = get_log_file()
  idx = 0
  f = open( logfnm, 'r' )
  keptlines = list()
  for line in f:
    keptlines.append( line )
    idx = idx + 1
    if idx >= keeplines:
      break
  f.close()
  f = open( logfnm, 'w' )
  for line in keptlines:
    f.write( line )
  f.close()
  set_log_file( logfnm, proclog_logger )
  
storedstdout = None
storedstderr = None

def redirect_stdout():
  """Stdout-stderr redirection

  * Forces stdout to point to odpy.proclog_logger
  * Forces stderr to point to odpy.syslog_logger

  Notes:
    * Changes the value of sys.stdout and sys.stderr
    * Should be avoided as much as possible: To be used only when one cannot
      redirect in any other way.

  """
  if (logconfig is  None) or (not logging.getLogger() == logconfig.root_logger):
    return
  if has_log_file():
    global storedstdout
    storedstdout = sys.stdout
    sys.stdout = open( get_log_file(), 'a' )
  if has_stdlog_file():
    global storedstderr
    storedstderr = sys.stderr
    sys.stderr = open( get_stdlog_file(), 'a' )

def restore_stdout():
  """Stdout-stderr restore

  Undo operation of redirect_stdout

  """

  if (logconfig is None) or (not logging.getLogger() == logconfig.root_logger):
    return
  if has_log_file():
    global storedstdout
    if storedstdout == None:
      sys.stdout = sys.__stdout__
    else:
      sys.stdout = storedstdout
      storedstdout = None
  if has_stdlog_file():
    global storedstderr
    if storedstderr == None:
      sys.stderr = sys.__stderr__
    else:
      sys.stderr = storedstderr
      storedstderr = None

def isWin():
  """Is platform Windows?

  Returns:
    * True if running on any Windows platform

  """

  return platform.system() == 'Windows'

def isLux():
  """Is platform Linux?

  Returns:
    * True if running on any Linux platform

  """

  return platform.system() == 'Linux'

def isMac():
  """Is platform Mac?

  Returns:
    * True if running on any Mac-OS platform

  """

  return platform.system() == 'Darwin'

if platform.python_version() < "3":
  std_msg( "odpy requires at least Python 3" )
  sys.exit( 1 )
  
def isPossibleODSoftwareDir( curdir ):
  relinfodir = 'relinfo'
  if not isMac():
    appldir = os.path.join(curdir, relinfodir)
    return os.path.isdir(appldir)
  
  appldir = os.path.join(curdir, "Resources", relinfodir)
  if os.path.isdir(appldir):
    return True
  return False


def getODSoftwareDir(args=None):
  """OpendTect sofware directory

  Parameters:
    * args (dict, optional):
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * str: Full path to the OpendTect software installation

  Notes:
    * First search method: retrieved from the input dictionary.
    * Second search method:  if odpy is located within an OpendTect
      installation, the path to this installation will be returned.
    * Third search method: retrieved by reading the 'DTECT_APPL'
      variables which are set by OpendTect at runtime.
    * Fourth search method: If all everything else fails, the PATH
      variable will be inspected to detect available OpendTect
      installations.

  Examples:
    >>> getODSoftwareDir()
    Windows: 'C:\\Program Files\\OpendTect\\2025'
    Linux: '/home/user/OpendTect/2025'
    MacOS: '/Applications/OpendTect/OpendTect 2025.app/Contents'

  """

  if args != None and 'dtectexec' in args:
    appldir = getExecPlfDir(args)
    for i in range(5):
      if isPossibleODSoftwareDir( appldir ):
        return appldir
      appldir = os.path.dirname(appldir)
  
  curdir = __file__
  for _ in range(4):
    curdir = os.path.dirname( curdir )
    if isPossibleODSoftwareDir( curdir ):
      return curdir

  applenvvar = 'DTECT_APPL'
  if applenvvar in os.environ:
    return os.environ[applenvvar]
 
  return findODSoftwarePath()

def findODSoftwarePath():
  if isWin():
    expectedpathends = [os.path.join("bin", "win64", "Release"),
                       os.path.join("bin", "win64", "Debug")]
  elif isLux():
    expectedpathends = [os.path.join("bin", "lux64", "Release"),
                       os.path.join("bin", "lux64", "Debug")]
  elif isMac():
    expectedpathends = [os.path.join("MacOS"),
                       os.path.join("MacOS", "Debug")]

  envpaths = os.environ.get('PATH', '').split(os.pathsep)
  for path in envpaths:
    for expectedpathend in expectedpathends:
      if path.endswith(expectedpathend):
        for _ in range(5):
          if isPossibleODSoftwareDir( path ):
            return path 
          path = os.path.dirname(path)
  return None

class BuildConfig(Enum):
  AUTO = 0
  Release = 1
  Debug = 2

def getExecPlfDir(args=None, config=BuildConfig.AUTO):
  """OpendTect executables directory

  Parameters:
    * args (dict, optional):
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * str: Full path to the binaries of an OpendTect installation

  Notes:
    * Assumes that the software installation can be located with getODSoftwareDir()
      and that python is running on a platform supported by OpendTect.

  Examples:
    >>> getExecPlfDir()
    Windows: 'C:\\Program Files\\OpendTect\\2025\\bin\\win64\\Release'
    Linux: '/home/user/OpendTect/2025/bin/lux64/Release'
    MacOS: '/Applications/OpendTect/OpendTect 2025.app/Contents/MacOS'

  """

  if args != None and 'dtectexec' in args and args['dtectexec'] != None:
    return args['dtectexec'][0]

  if config==BuildConfig.AUTO:
    relexecpath = getExecPlfDir( args, BuildConfig.Release )
    if relexecpath == None:
      return getExecPlfDir( args, BuildConfig.Debug )
    return relexecpath

  appldir = getODSoftwareDir()
  paths = [] 
  
  if isWin():
    if config == BuildConfig.Release:
      paths.append( os.path.join("bin", "win64", "Release", "od_FileBrowser.exe") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("bin", "win64", "Debug", "od_FileBrowserd.exe") )
      paths.append( os.path.join("bin", "win64", "Debug", "od_FileBrowser.exe") )
  
  elif isLux(): 
    if config == BuildConfig.Release:
      paths.append( os.path.join("bin", "lux64", "Release", "od_FileBrowser") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("bin", "lux64", "Debug", "od_FileBrowserd") )
      paths.append( os.path.join("bin", "lux64", "Debug", "od_FileBrowser") )
  
  elif isMac():
    if config == BuildConfig.Release:
      paths.append( os.path.join("MacOS", "od_FileBrowser") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("MacOS", "Debug", "od_FileBrowserd") )
      paths.append( os.path.join("MacOS", "Debug", "od_FileBrowser") )

  for path in paths:
    fullpath = os.path.join(appldir, path)
    if os.path.isfile(fullpath):
      return os.path.dirname(fullpath)

  return None
  
def getODBindLib(args=None, config=BuildConfig.AUTO):
  """OpendTect ODBind link library path

  Parameters:
    * args (dict, optional):
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * str: Full path to the ODBind library of an OpendTect installation

  Examples:
    >>> getODBindLib()
    Windows: 'C:\\Program Files\\OpendTect\\2025\\bin\\win64\\Release\\ODBind.dll'
    Linux: '/home/user/OpendTect/2025/bin/lux64/Release/libODBind.so'
    MacOS: '/Applications/OpendTect/OpendTect 2025.app/Contents/Frameworks/libODBind.dylib'
  
  """

  if config==BuildConfig.AUTO:
    odb_path = getODBindLib( args, BuildConfig.Release )
    if odb_path == None:
      return getODBindLib( args, BuildConfig.Debug )
    return odb_path

  appldir = getODSoftwareDir()
  paths = [] 
  
  if isWin():
    if config == BuildConfig.Release:
      paths.append( os.path.join("bin", "win64", "Release", "ODBind.dll") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("bin", "win64", "Debug", "ODBindd.dll") )
      paths.append( os.path.join("bin", "win64", "Debug", "ODBind.dll") )
  
  elif isLux(): 
    if config == BuildConfig.Release:
      paths.append( os.path.join("bin", "lux64", "Release", "libODBind.so") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("bin", "lux64", "Debug", "libODBindd.so") )
      paths.append( os.path.join("bin", "lux64", "Debug", "libODBind.so") )
  
  elif isMac():
    if config == BuildConfig.Release:
      paths.append( os.path.join("Frameworks", "libODBind.dylib") )
    elif config == BuildConfig.Debug:
      paths.append( os.path.join("Frameworks", "Debug", "libODBindd.dylib") )
      paths.append( os.path.join("Frameworks", "Debug", "libODBind.dylib") )

  for path in paths:
    fullpath = os.path.join(appldir, path)
    if os.path.isfile(fullpath):
      return fullpath

  return None

def getLibPlfDir(args=None, config=BuildConfig.AUTO):
  """OpendTect link libraries directory

  Parameters:
    * args (dict, optional):
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * str: Full path to the libraries of an OpendTect installation

  Examples:
    >>> getLibPlfDir()
    Windows: 'C:\\Program Files\\OpendTect\\2025\\bin\\win64\\Release'
    Linux: '/home/user/OpendTect/2025/bin/lux64/Release'
    MacOS: '/Applications/OpendTect/OpendTect 2025.app/Contents/Frameworks'
  
  """

  libpath = getODBindLib(args, config)
  if libpath and os.path.isfile(libpath):
    return os.path.dirname(libpath)
  
  return None

def get_settings_dir():
  """Directory with the OpendTect user settings

  Parameters
  ------
  Can be overruled by setting the
  environment variable DTECT_PERSONAL_DIR

  Returns
  ------
  Full path to $HOME/.od

  """
  if 'DTECT_PERSONAL_DIR' in os.environ:
    return os.environ['DTECT_PERSONAL_DIR']
  ret = os.path.join( '~', '.od' )
  return os.path.expanduser( ret )

def get_settings_filename( filenm='settings' ):
  """Get file path to an OpendTect settings file

  Parameters
  ----------
    * filenm (string, optional): base file name inside .od folder
    default is 'settings'
    Will be influenced by the environment variable DTECT_USER if
    set.

  Returns
  ------
  Full path to $HOME/.od/filenm[.DTECT_USER]

  """
  if 'DTECT_USER' in os.environ:
    filenm += '.' + os.environ['DTECT_USER']
  return os.path.join( get_settings_dir(), filenm )

def get_base_datadir():
  """Get the OpendTect Survey Data Root directory

  Parameters
  ----------
  Can be overruled by setting the
  environment variable DTECT_DATA

  Returns
  ------
  Full path to the Opendtect Survey Data Root
  as written inside from get_settings_filename()

  """
  if isWin():
    if 'DTECT_WINDATA' in os.environ:
      appldata = os.environ['DTECT_WINDATA']
      if os.path.isdir(appldata):
        return appldata
  if 'DTECT_DATA' in os.environ:
    appldata = os.environ['DTECT_DATA']
    if os.path.isdir(appldata):
      return appldata
  settsfnm = get_settings_filename()
  if os.path.isfile(settsfnm):
    from odpy.iopar import read_from_iopar
    return read_from_iopar( settsfnm, 'Default DATA directory' )
  return None

def get_surveydir():
  """Get the OpendTect Current Survey directory

  Returns
  -------
  Directory name of the current survey as written inside
  get_settings_filename( 'survey' )

  """
  survfnm = get_settings_filename( filenm='survey' )
  if os.path.isfile(survfnm):
    with open( survfnm, 'r' ) as fp:
      return fp.readline()
  return None

def get_data_dir():
  """Full path to the current OpendTect Survey directory

  Returns
  ------
  Full path to the current survey as retrieved by
  get_base_datadir() and get_surveydir()

  """
  return os.path.join( get_base_datadir(), get_surveydir() )

def add_user_dtectdata( args=None ):
  """Returns the OpendTect Survey Data Root in a dictionary

  Parameters
  ----------
    * args (dict, optional)
      Dictionary where the returned value is added/updated

  Returns
  -------
    Dictionary with the member 'dtectdata'. The value
    for that member should point to the return of get_base_datadir()

  """
  dtectdatadir = get_base_datadir()
  if dtectdatadir != None:
    if args == None:
      args = {'dtectdata': [dtectdatadir]}
    else:
      args.update({'dtectdata': [dtectdatadir]})
  return args 

def add_user_survey( args=None ):
  """Returns the OpendTect Survey Directory in a dictionary

  Parameters
  ----------
  * args (dict, optional)
    Dictionary where the returned value is added/updated

  Returns
  -------
  Dictionary with the member 'survey'. The value
  for that member should point to the return of get_surveydir()

  """
  surveydir = get_surveydir()
  if surveydir != None:
    if args == None:
      args = {'survey': [surveydir]}
    else:
      args.update({'survey': [surveydir]})
  return args

def getODArgs(args=None):
  """OpendTect arguments dictionary

  Create a dictionary that contains typical OpendTect
  command line arguments and the files from this module' loggers

  Parameters:
    * args (dict, optional):
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * dict: A dictionary with the following key-values:
        * 'dtectexec' : Full path to the OpendTect installation (see getExecPlfDir)
        * 'dtectdata' : The root projects directory name
        * 'survey' : The survey directory name
        * 'proclog' : The log file from proclog_logger if applicable
        * 'syslog' : The log file frol syslog_logger if applicable

  """

  ret = {
    'dtectexec': [getExecPlfDir(args)]
  }
  if args == None or ('dtectdata' in args and args['dtectdata'] == None):
    ret = add_user_dtectdata( ret )
  elif args != None and 'dtectdata' in args:
    ret.update({'dtectdata': args['dtectdata']})
  if args == None or ('survey' in args and args['survey'] == None):
    ret = add_user_survey( ret )
  elif args != None and 'survey' in args:
    ret.update({'survey': args['survey']})
  if has_log_file() :
    ret.update({'proclog': args['logfile'].name})
  if has_stdlog_file():
    ret.update({'syslog': args['sysout'].name})
#  else:
#    if has_log_file():
#      ret.update({'syslog': args['logfile'].name})
  return ret

def getIconFp(nm,args=None):
  """Path to an OpendTect icon file

  Parameters:
    * nm (string): Icon file basename (without extension)
    * args (dict, optional)
      Dictionary with the member 'dtectexec'. The value
      for that member should point to the executables folder
      of the requested application

  Returns:
    * str: Full path to the icon folder of the OpendTect installation

  Notes:
    Assumes that the software installation can be located with getODSoftwareDir()

  Examples:
    >>> getIconFp( 'dgbpro' )
    'C:\\Program Files\\OpendTect\\6.6.0\\data\\icons.Default\\dgbpro.png'
    
  """
  oddir = getODSoftwareDir(args)
  ret = os.path.join(oddir,'data','icons.Default',nm)+'.png'
  if os.path.isfile(ret):
    return ret
  return None

def tail(fp,lines=1,strip_empty=False,_buffer=4098):
  """ Returns the last line(s) from a file

  Parameters:
    * fp (object): opened log file
    * lines (int): number of last lines in a file to be printed
    strip_empty (bool): removes empty new lines if True
    buffer (int): 
  """
  
  lines_found = []
  block_counter = -1
  while len(lines_found) < lines:
    try:
      fp.seek(block_counter * _buffer, os.SEEK_END)
    except IOError:
      fp.seek(0)
      lines_found = fp.readlines()
      break

    lines_found = fp.readlines()
    block_counter -= 1

  ret = lines_found[-lines:]
  if strip_empty:
    while '\n' in ret:
      ret.remove('\n')
  return ret

def batchIsFinished( logfile ):
  """OpendTect batch processing status

  Checks if an OpendTect batch process reached completion by
  parsing its log file.

  Parameters:
    logfile (str): Full path to an existing OpendTect log file.

  Returns:
    * bool:
      True if the file exists and contains 'Finished batch processing' at its tail.

  Notes:
    Instantaneous status. To monitor if the processing finishes,
    the user must repeatedly call this function.

  """

  ret = list()
  with open(logfile) as fd:
    ret = tail(fd,10,True)
  return len(ret) > 0 and 'Finished batch processing' in ret[-1]

def writeFile( fnm, content ):
  """ Creates a new file with contents

  Parameters:
    fnm (str): name of file to be created/written to
    content (str): content to be added to the file

  Returns:
    * bool:
      True if file has been successfully created
      False if file isn't created due to an error
  
  """
  try:
    f = open( fnm, 'w' )
    f.write( content )
    f.close()
  except:
    return False
  return True

class Timer(threading.Timer):
    """Repeated timer

    Timer that restarts automatically after each interval
    """

    def run(self):
        while not self.finished.is_set():
            self.finished.wait(self.interval)
            self.function(*self.args, **self.kwargs)
        self.finished.set()
