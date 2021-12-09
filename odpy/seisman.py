from odpy.oscommand import getODCommand
import odpy.common as odcommon
import odpy.dbman as oddbman
import odpy.iopar as iopar

seismanexe = 'od_DBMan'                                                                                                                       
seisdbdirid = '100010'                                                                                                                           
seistrlgrp = 'Seismic Data'                                                                                                                              
dgbtrl = 'dGB'

dblist = None

def getSeismicDBList( reload, args=None ):
    """ Gets information on available seismics from database for a survey

    Parameters:
        * reload (boolean, optional): Force re-reading of the database files (no caching allowed)
        * args (dictionary, optional): Dictionary of optional parameters (see odpy.common).
            Default to None.

    Returns:
        dict: containing information on survey seismic (size, IDs, Names, Status, etc)
    """

    global dblist
    if dblist != None and not reload:
        return dblist
    
    if args == None:
        args = odcommon.getODArgs()
    dblist = oddbman.getDBList(seistrlgrp, exenm=seismanexe, args=args)
    return dblist

def getName( dbkey, args=None ):
  """ Gets seismic name

  Parameters:
    * dbkey (str): seismic database key
    * reload (boolean, optional): Force re-reading of the database files
          (no caching allowed). Default to False
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    * str: seismic data name

  """

  cmd = getODCommand(seismanexe,args=args)
  cmd.append( '--info' )
  cmd.append( dbkey )
  ret = oddbman.getDBDict( cmd, args=args )
  return ret['Name']

def getDBKey( seisnm, reload=False, args=None ):
  """ Gets well database key

  Parameters:
    * seisnm (str): seismic name
    * reload (boolean, optional): Force re-reading of the database files
          (no caching allowed). Default to False
    * args (dictionary, optional): Dictionary of optional parameters (see common).
          Default to None.

  Returns:
    str: Database key for seismic name provided
  """

  global dblist
  dblist = getSeismicDBList(reload,args)
  return oddbman.getDBKeyForName(dblist, seisnm)  

def get_file_location(dbname):
    """ Gets file location of seismi data

    Parameters:
        * dbname (str): seismic name

    Returns:
        str: full path to seismic data
    """

    fileloc = oddbman.getFileLocation(getDBKey(dbname))
    return iopar.read_from_iopar(fileloc, 'File name')

def isPresent(dbname):
    """
    Checks if seismic data exists in survey

    Parameters:
        dbname (str): seismic data name

    Returns:
        bool: True if seismic data is found in survey, False if otherwise
    """

    dblist = getSeismicDBList(reload=False)
    if dbname in dblist['Names']:
        return True
    else:
        return False