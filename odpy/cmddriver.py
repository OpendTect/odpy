import odpy.oscommand as odcommand

driverexe = 'od_main'

def doScript( filepath, args=None):
    """ Executes a script in OpendTect
    """
    cmd = []
    command = odcommand.getODCommand( driverexe, args=args )
    cmd.append( command)
    cmd.append( '--cmd' )
    cmd.append( filepath )
    return odcommand.execCommand( cmd, env=odcommand.getEnvForOpendTect(args=args) )

def hasError( filepath ):
    with open(filepath, 'r') as f:
        for line in f:
            if 'error' in line.lower():
                return True
        return False
