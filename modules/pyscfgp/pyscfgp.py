#! /usr/bin/env python

class scfgp:
    import os
    import sys
    
    def __init__( self, _verbose=False ):
        self.verbose = _verbose
        if self.verbose:
            print( '[PYSCFGP] Initialize' )
        self.configFiles = []
        self.data = []
        self.config_files = 0

    def addConfigFile( self,_filename ):
        self.config_files = 0
        if self.os.path.isfile( _filename ):
            file = open( _filename, 'r' )
            self.configFiles.append( [file, _filename] )
            if self.verbose:
                print( '[PYSCFGP] Adding %s to config files list.' % _filename )
                self.config_files += 1
        else:
            if self.verbose:
                print( '[PYSCFGP] Cannot find/open %s! Skip.' % _filename )

    def listConfigFiles( self ):
        if self.verbose:
            print( '[PYSCFGP] Available config files:' )
            for entry in self.configFiles:
                print( ' -> %s' % entry[1] )

    def readConfigFiles( self ):
        if self.config_files == 0:
#            print( '[PYSCFGP] No config files available!' )
            raise ValueError( 'No config files available!' )
        else:
            if self.verbose:
                print( '[PYSCFGP] Reading config files.' )
            for f in self.configFiles:
                for line in f[0].readlines( ):
                    self.readLine( line )

    def readLine( self, line ):
        dataRead = line.split()        
        if dataRead[0] == '#' or len( dataRead ) > 2:
            pass
        else:
            if self.verbose:
                print( 'Read %s parameters with value: %s' % (dataRead[0], dataRead[1]) )
            self.data.append( dataRead )

    def get( self, name, defaultValue ):
        for data in self.data:
            if data[0] == name:
                if self.verbose:
                    print( '[PYSCFGP] Found %s parameter.' % name )
                return data[1]
            else:
                if self.verbose:
                    print( '[PYSCFGP] Did not found %s parameter. Returning default value.' % data[0] )
                return defaultValue
