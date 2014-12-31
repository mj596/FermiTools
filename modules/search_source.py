class SearchSource( ):
    # get rid of UserWarning when importing astropy
    import warnings
    warnings.filterwarnings('ignore', '.*ICRS.*',)

    from modules.exceptions.exceptions import SourceNotFound, ModuleNotFound

    def __init__( self ):
        self.source_name = ''

        self.list_search_db = [ "NED", "Simbad", "Vizier" ]
        self.db = self.list_search_db[0]

    def set_source( self, _source_name ):
        self.source_name = _source_name        

    def get_db( self ):
        return self.db

    def set_db( self, _db ):
        if _db in self.list_search_db:
            self.db = _db
        else:
            self.error_message( 'No such database! Setting %s' % self.db )

    def info_message( self, text ):
        print( '[SearchSource] ' + text )

    def error_message( self, text ):
        print( '[SearchSource] ERROR ' + text )
        
    def get_source_info( self ):
        name = 'None'
        ra = '0.0'
        dec = '0.0'

        if self.source_name != '':
            if self.db != '':
                self.info_message( 'Searching %s in %s database ...' % ( self.source_name, self.db ) )
                try:
                    if self.db == 'NED':
                        ( name, ra, dec ) = self.get_source_info_NED( self.source_name )
                    elif self.db == 'Vizier':
                        self.error_message( 'Not implemented yet!' )
                    elif self.db == 'Simbad':
                        ( name, ra, dec ) = self.get_source_info_Simbad( self.source_name )

                except self.SourceNotFound as error:
                    self.error_message( 'Could not find %s!' % error.source_name )
                except self.ModuleNotFound as error:
                    self.error_message( 'Could not import %s!' % error.module_name )

                self.source_name = name 
                
                self.info_message( 'Done' )
                
            else:
                self.info_message( ' ' )
                self.error_message( 'No database selected' )

        else:
            self.error_message( 'No target selected.' )
            
        return ( name, ra, dec )

    def get_source_info_NED( self, name ):
        try:
            from astroquery.ned import Ned
            import astroquery.exceptions

            result_table = Ned.query_object( name )
            name = result_table['Object Name'][0]
            ra = result_table['RA(deg)'][0]
            dec = result_table['DEC(deg)'][0]

            return ( name, ra, dec )

        except ImportError:
            raise self.ModuleNotFound( 'astroquery' )
            return ( '', 0.0, 0.0 )
        except ( astroquery.exceptions.RemoteServiceError, Exception ):
            raise self.SourceNotFound( name )
            return ( '', 0.0, 0.0 )

    def get_source_info_Simbad( self, name ):
        try:
            from astroquery.simbad import Simbad
            import astroquery.exceptions

        except ImportError:
            raise self.ModuleNotFound( 'astroquery' )
            return ( '', 0.0, 0.0 )
        try:
           from astropy.coordinates import ICRS
        except ImportError:
            raise self.ModuleNotFound( 'astropy.coordinated' )
            return ( '', 0.0, 0.0 )
        try:
            result_table = Simbad.query_object( name )
            name = result_table['MAIN_ID'][0]
            ra = result_table['RA'][0]
            dec = result_table['DEC'][0]
        
            icrs = ICRS( self.convert_ra_from_simbad( ra ), self.convert_dec_from_simbad( dec ) )
            return ( name, icrs.ra.deg, icrs.dec.deg )

        except ( astroquery.exceptions.RemoteServiceError, Exception ):
            raise self.SourceNotFound( name )
            return ( '', 0.0, 0.0 )

    def get_source_info_Simbad( self, name ):
        
        try:
            from astroquery.simbad import Simbad
            import astroquery.exceptions

        except ImportError:
            raise self.ModuleNotFound( 'astroquery' )
            return ( '', 0.0, 0.0 )
        try:
           from astropy.coordinates import ICRS
        except ImportError:
            raise self.ModuleNotFound( 'astropy.coordinated' )
            return ( '', 0.0, 0.0 )
        try:
            result_table = Simbad.query_object( name )
            name = result_table['MAIN_ID'][0]
            ra = result_table['RA'][0]
            dec = result_table['DEC'][0]
        
            icrs = ICRS( self.convert_ra_from_simbad( ra ), self.convert_dec_from_simbad( dec ) )
            return ( name, icrs.ra.deg, icrs.dec.deg )

        except ( astroquery.exceptions.RemoteServiceError, Exception ):
            raise self.SourceNotFound( name )
            return ( '', 0.0, 0.0 )

    def convert_ra_from_simbad( self, ra ):
        counter = 0
        converted_ra = ''
        for i in ra:
            if i == ' ' and counter == 0:
                converted_ra += 'h'
                counter+=1
            elif i == ' ' and counter == 1:
                converted_ra += 'm'
                counter+=1
            else:
                converted_ra += i
        converted_ra += 's'
            
        return converted_ra
                        
    def convert_dec_from_simbad( self, dec ):
        counter = 0
        converted_dec = ''
        for i in dec:
            if i == ' ' and counter == 0:
                converted_dec += 'd'
                counter+=1
            elif i == ' ' and counter == 1:
                converted_dec += 'm'
                counter+=1
            else:
                converted_dec += i
        converted_dec += 's'
            
        return converted_dec




