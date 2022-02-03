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

def getDBKey( seisnm, reload=True, args=None ):
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
    """ Gets file location of seismic data

    Parameters:
        * dbname (str): seismic name

    Returns:
        str: full path to seismic data
    """
    
    fileloc = oddbman.getFileLocation(getDBKey(dbname))
    if '.sgydef' in fileloc:
        return iopar.read_from_iopar(fileloc, 'File name')
    else:
        return fileloc

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

def show_line(data, ranges, figsize, inline=False, xline=False, Z=False):
    """
    Displays 2D visualization of either inline, crossline, or Z/time slice

    Parameters:
        * data (array): 3d numpy array of data (time/depth, crossline, inline)
        * ranges (dict): specifying survey ranges (with keys inline, xline, Z)
        * figsize (tuple): width and height specifications for figure
        * inline, xline, Z (int): inline, xline, or time slice to be displayed

    Note: either inline or xline or Z can be displayed once. other dimensions retain their default
            False value when a dimension is selected/displayed

    Returns: None (figure is displayed)
    """

    import matplotlib.pyplot as plt
    fig = plt.figure(figsize=figsize)
    if inline:
        plt.imshow(data[:, :, inline], cmap='seismic_r', 
                   extent=(ranges['xline'][0], ranges['xline'][1], 
                           ranges['Z'][0], ranges['Z'][1]))
    if xline:
        plt.imshow(data[:, xline, :], cmap='seismic_r',
                   extent=(ranges['inline'][0], ranges['inline'][1], 
                           ranges['Z'][0], ranges['Z'][1]))
    if Z:
        plt.imshow(data[Z, :, :], cmap='seismic_r',
                   extent=(ranges['xline'][0], ranges['xline'][1], 
                           ranges['inline'][0], ranges['inline'][1]))

def ConvertSegy2Numpy(filename: str):
    """ converts segy data to numpy array

    Parameters:
        * filename (str): path to segy data in sgy or segy, zgy format

    Returns:
        * ndarray: of segy data
    """
    import segyio
    with segyio.open(filename) as segyfile:
        return segyio.tools.cube(segyfile)                           