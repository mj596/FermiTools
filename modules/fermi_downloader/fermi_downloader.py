from astroquery import fermi
    
class FermiData( ):
    from modules.exceptions.exceptions import ModuleNotFound

    def __init__( self ):
        self.name_or_coords = ''
        self.searchradius = 1.0
        self.obsdates = ''
        self.timesys = 'MET'
        self.energyrange = ''
        self.files_to_download = []
        self.result_page = None
        self.spacecraftdata = True

    def set_coords( self, ra, dec ):
        self.name_or_coords = str(ra) + ', ' + str(dec)

    def set_roi( self, roi ):
        self.searchradius = str( roi )

    def set_time( self, tmin, tmax ):
        self.obsdates = str( int(tmin) ) + ', ' + str( int(tmax) )

    def set_energy( self, emin, emax ):
        self.energyrange = str( emin ) + ', ' + str( emax )

    def set_spacecraft( self, select ):
        self.spacecraftdata = select

    def get_data( self ):
#        print( 'Attempting: ' )
#        print( 'fermi.FermiLAT.query_object( name_or_coords = \'' + str( self.name_or_coords ) +'\', energyrange_MeV = \'' + str( self.energyrange ) + '\', searchradius = \'' + str( self.searchradius ) + '\', obsdates = \'' + str( self.obsdates ) + '\', timesys = \'' + str( self.timesys ) + '\' )' )
        self.info_message( 'Getting results from LAT Data Server - this may take a while depending on the size of requested data. Be patient.' )

        result = fermi.FermiLAT.query_object( name_or_coords = self.name_or_coords, energyrange_MeV = self.energyrange, searchradius = self.searchradius, obsdates = self.obsdates, timesys = self.timesys )

        self.result_page = fermi.FermiLAT.query_object_async( name_or_coords = self.name_or_coords, energyrange_MeV = self.energyrange, searchradius = self.searchradius, obsdates = self.obsdates, timesys = self.timesys )

        self.files_to_download = []
        
        for i in result:
            self.files_to_download.append( i )
        
        self.info_message( 'Done' )

#    def save_fermi_filelist( self ):

    def get_files_to_download( self ):
        return self.files_to_download

    def get_download_webpage( self ):
        return self.result_page

    def info_message( self, text ):
        print( text )

    def error_message( self, text ):
        print( text )
