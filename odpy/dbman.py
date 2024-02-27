import json

import odbind as odb
from odbind.survey import Survey

def getSurvey( args={} ):
  """Return an odbind.Survey instance using the content of args , falling bask to the current users 
  settings for base data folder and current survey.

  Parameters:
    * args (dict, optional):
      Dictionary with the members 'dtectdata' and 'survey' as 
      single element lists, and/or 'dtectexec' (see odpy.common.getODSoftwareDir)

  Returns:
    odbind.Survey

  """
  return Survey(args.get('survey',[odb.get_user_survey()])[0], args.get('dtectdata', [None])[0])

def getDBList(translnm,alltrlsgrps=False,args={}):
  """ Gets information on survey database items

  Parameters:
    * translnm (string): 
    * alltrlsgrps (bool): if True, returns information on all translators in the TranslatorGroup
    * args (dict, optional):
      Dictionary with the members 'dtectdata' and 'survey' as 
      single element lists, and/or 'dtectexec' (see odpy.common.getODSoftwareDir)

  Returns:
    * list[dict]: List of Python dictionaries containing database information {ID, Name, Format, TranslatorGroup, File name}
  """

  surv = getSurvey(args)
  return surv.get_object_infos(translnm, alltrlsgrps)

def getInfoFromDBListByNameOrKey(nm_or_key,dblist):
  """ Gets info from database list with obj key or name

  Parameters:
    * nm_or_key (str): object key or name
    * dblist (dict): survey database list, check odpy.getDBList for docs

  Returns:
    * dict: info on database object (Name,ID, Format, Type, TranslatorGroup iff available)
  """

  ret = list(filter(lambda item: item['ID']==nm_or_key or item['Name']==nm_or_key, dblist))
  return ret[0] if len(ret)>0 else {}
  
def getInfoByName(objnm,translnm=None, args={} ):
  """ Gets object info by name

  Parameters:
    * objnm (str): database object to get info on
    * translnm (str):
    * args (dict, optional):
      Dictionary with the members 'dtectdata' and 'survey' as 
      single element lists, and/or 'dtectexec' (see odpy.common.getODSoftwareDir)

  Returns:
    * dict: information on object, dict keys include; ID, Name, file name, etc

  Example:
  >>> import odpy.dbman as dbman
  >>> dbman.getInfoByName(objnm='F02-1', translnm='Well')
      {'ID': '100050.2',
       'Name': 'F02-1',
       'Format': 'dGB',
       'TranslatorGroup': 'Well',
       'File_name': 'C:\\DTECT_DATA\\F3_Demo_2020\\WellInfo\\F02-1.well',
       'Status': 'OK'}

  """
  surv = getSurvey(args)
  ret = surv.get_object_info(objnm, translnm)
  if not 'ID' in ret:
    return None
  return ret

def getInfoByKey(objkey,args={} ):
  """ Gets datbase info on well

  Parameters:
    * objkey (str): well ID key
    * args (dict, optional):
      Dictionary with the members 'dtectdata' and 'survey' as 
      single element lists, and/or 'dtectexec' (see odpy.common.getODSoftwareDir)

  Returns:
    dict: file info (ID, Name, Format, File name, etc)
  """

  surv = getSurvey(args)
  ret = surv.get_object_info_byid(objkey)
  if not 'ID' in ret:
    return None
  return ret

def getByName( dblist, retname, keystr ):
  """ Gets value of specified database list key

  Parameters:
    * dblist (dict): survey database list, check odpy.getDBList for docs
    * retname (str): key to return from dblist
    * keystr (str): value to return from retname

  Returns:
    * str: database object value

  Example:
  
  >>> import odpy.dbman as dbman
  >>> dbman.getByName(dblist, 'F03-4', 'ID')
      '100050.4'

  """
  ret = getInfoFromDBListByNameOrKey(retname, dblist)
  return ret.get(keystr, None)

def getDBKeyForName( dblist, retname ):
  """ Gets object ID key from database info

  Parameters:
    * dblist (dict): survey database list, check odpy.getDBList for docs
    * retname (str): key to return from dblist

  Returns:
    * str: ID of database object (well)

  """

  return getByName( dblist, retname, 'ID' )

def getFileLocation( dbkey, args={} ):
  """  Gets full file path

  Parameters:
    * dbkey (str): object database key
    * args (dict, optional):
      Dictionary with the members 'dtectdata' and 'survey' as 
      single element lists, and/or 'dtectexec' (see odpy.common.getODSoftwareDir)

  Returns:
    str: full path to file

  """

  return getInfoByKey(dbkey, args=args).get('File name', None)

def getNewEntryFileName( objnm, trgrp, trl, overwrite=False, args={} ):
  """ Registers a new OpendTect dataset to database

  Parameters:
    * objnm (str): the object name
    * trgrp (str): TranslatorGroup e.g. Well, Seismic Data, etc
    * trl (str): Translator e.g. CBVS

  Returns:
    * file path to the object created with write permission

  """

  surv = getSurvey(args)
  surv.create_object(objnm, trgrp, trl, overwrite)
  newobj = surv.get_object_info(objnm, trgrp)
  return newobj['File name']

def removeEntry(objname, trgrp=None, args={}):
  """ Remove the OpendTect dataset from the database

  Parameters:
    * objname (str): the object name
    * trgrp (str)=None: TranslatorGroup

  """

  surv = getSurvey(args)
  surv.remove_object(objname, trgrp)

def isPresent(objname, trgrp=None, args={}):
  """ Checks if an OpendTect dataset exists in the database

  Parameters:
    * objname (str): the object name
    * trgrp (str)=None: TranslatorGroup

  Returns:
    * True if the object exists, False otherwise
  
  """

  surv = getSurvey(args)
  return surv.has_object(objname, trgrp)
