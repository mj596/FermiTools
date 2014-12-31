class TimeConverter( ):
    import time

    def __init__( self ):
        self.error_iso_date = "1900-01-01 00:00:00"
        self.iso8601format = "%Y-%m-%d %H:%M:%S"
        self.default_epoch = self.time.strftime( self.iso8601format, self.time.localtime(0) )
        self.timezone_correction_seconds = self.time.mktime( self.time.gmtime(0) ) - self.time.mktime( self.time.localtime(0) )
        self.fermi_epoch_utc = "2001-01-01 00:00:00"
        self.fermi_epoch_localtime = self.time.strftime( self.iso8601format, self.time.localtime( self.time.mktime( self.time.strptime( self.fermi_epoch_utc, self.iso8601format ) ) + self.timezone_correction_seconds ) )
        self.current_epoch = self.default_epoch
        self.mission = 'default'

    def set_mission( self, _mission ):
        self.mission = _mission
        if self.mission == 'Fermi' or self.mission == 'fermi':
            self.current_epoch = self.fermi_epoch_localtime

        if self.mission == 'Default' or self.mission == 'default':
            self.current_epoch = self.default_epoch

    def convert_iso_to_seconds( self, _time ):
        tuple_time_default_epoch = self.time.strptime( str(_time), self.iso8601format )
        seconds_time_default_epoch = self.time.mktime( tuple_time_default_epoch )
        tuple_time_current_epoch = self.time.strptime( self.current_epoch, self.iso8601format )
        seconds_time_current_epoch = self.time.mktime( tuple_time_current_epoch )
        time_MET = seconds_time_default_epoch - seconds_time_current_epoch
        return str( time_MET )
        
    def convert_seconds_to_iso( self, _time ):
        current_epoch = self.current_epoch
        self.current_epoch = self.default_epoch
        try:
            seconds_since_default_epoch = float( self.convert_iso_to_seconds( current_epoch ) ) + float( _time )
            tuple_time = self.time.localtime( seconds_since_default_epoch )
            self.current_epoch = current_epoch
            return self.time.strftime( self.iso8601format, tuple_time )

        except ValueError:
            self.current_epoch = current_epoch
            return self.error_iso_date

    def get_current_time( self ):
        current_epoch = self.current_epoch
        self.current_epoch = self.default_epoch
        try:
            seconds_since_default_epoch = self.time.time( ) - float( self.convert_iso_to_seconds( current_epoch ) )
            self.current_epoch = current_epoch
            return seconds_since_default_epoch
        except ValueError:
            self.current_epoch = current_epoch
            return self.error_iso_date

    

