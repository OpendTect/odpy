"""
Copyright (C) dGB Beheer B.V.; (LICENSE) http://opendtect.org/OpendTect_license.txt
  * AUTHOR : A. Huck
  * DATE   : Nov 2018

Module Summary
###############

Tools database access and connection to survey wells and logs

Tutorial link can be found here: https://github.com/OpendTect/OpendTect-ML-Dev/blob/main/documentation/workflows/notebooks/odpy_wellman_tutorial.ipynb

"""

import odpy.common as odcommon
import odpy.dbman as oddbman
from odbind.well import Well

wlltrlgrp = 'Well'
dblist = {}

def getNames( args={} ):
  """ Gets survey well names from database

  Parameters:
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    * list: list of available survey wells from database


  """

  if not args:
    args = odcommon.getODArgs()

  surv = oddbman.getSurvey(args)
  return Well.names(surv)

def getInfo( wllnm, args={} ):
  """ Gets information for a well

  Parameters:
    * wllnm (str): well name from survey
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    * dict: information on well ID, name, x y cordinates, status etc

  """

  surv = oddbman.getSurvey(args)
  return Well(surv, wllnm).info()
  
def getName( dbkey, args={} ):
  """ Gets well name

  Parameters:
    * dbkey (str): well database key
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    * str: Well name

  """

  ret = oddbman.getInfoByKey(dbkey, args)
  return ret['Name']

def getLogNames( wllnm, args={} ):
  """ Gets logs available for a well

  Paramters:
    * wllnm (str): name of well
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    * list: list containing log names

  """

  surv = oddbman.getSurvey(args)
  return Well(surv, wllnm).log_names

def getLog( wllnm, lognm, args={} ):
  """Get a well log from the OpendTect database
    Read a single log from the OpendTect database, without
    any depth resampling or unit conversion.
    
    Parameters:
      * wllnm (string): Well database name
      * lognm (string): Log name as reported by getLogNames(wllnm)
      * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.
          
    Returns:
      tuple: Two arrays with depths (MD) and log values
    
  """

  surv = oddbman.getSurvey(args)
  res,_ = Well(surv, wllnm).logs([lognm], upscale=False)

  return (res['dah'], res[lognm])

def getLogs( wllnm, logidxlst, zstep=0.5, args={} ):
  """Get re-sampled logs from OpendTect

  Parameters:
      wllnm (string): Well database name
      logidxlst (string): List of log indices to be resampled
      zstep (double, optional): Resampling step in meters. Default to 0.5
      args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    dict: Dictionary with log names as keys, logs as numpy arrays.
        A depth array is also always output.

  Example:
     Get the logs from the well F03-4 with database indices 0, 1, 4, 6:
     >>> logs = odpy.wellman.getLogs( 'F03-4', '0`1`4`6' )

  """

  surv = oddbman.getSurvey(args)
  well = Well(surv, wllnm)
  alllogs = well.log_names
  logs = [alllogs[idx] for idx in logidxlst]
  res,_ = well.logs(logs, zstep=zstep, upscale=True)
  return res

def getDBKey( wllnm, args={} ):
  """ Gets well database key

  Parameters:
    * wllnm (str): well name
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    str: Database key for well name provided
  """

  ret = oddbman.getInfoByName(wllnm, wlltrlgrp, args)
  return ret['ID']  

def getWellDBList( reload=False, args={} ):
  """ Gets information on wells from database for a survey

  Parameters:
    * reload (boolean, optional): Force re-reading of the database files (no caching allowed)
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    dict: containing information on survey database wells (size, IDs, Names, Status, etc)
  """

  global dblist
  if dblist and not reload:
    return dblist

  if not args:
    args = odcommon.getODArgs()

  dblist = oddbman.getDBList(wlltrlgrp, args=args)
  return dblist

def getMarkers( wllnm, args={} ):
  """ Gets information on available markers for a well

  Parameters:
    * wllnm (str): well name
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    tuple: contains lists of available markers (names, MDs, colors)
  """

  surv = oddbman.getSurvey(args)
  markers = Well(surv, wllnm).marker_info()
  return ([marker['name'] for marker in markers], [marker['dah'] for marker in markers], [marker['color'] for marker in markers])
  
def getTrack( wllnm, args={} ):
  """ Gets well (track) depth information

  Parameters:
    * wllnm (str): well name
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

    Returns:
      tuple: contains lists of track depths (MDs, TVDSS, x coord., y coord.)

  """

  surv = oddbman.getSurvey(args)
  track = Well(surv, wllnm).track()
  return (track['dah'], track['tvdss'], track['x'], track['y'])

