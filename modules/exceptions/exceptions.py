class SourceNotFound( Exception ):
    def __init__( self, _source_name ):
        self.source_name = _source_name

class ModuleNotFound( Exception ):
    def __init__( self, _module_name ):
        self.module_name = _module_name

class RangeError( Exception ):
    def __init__( self, _error_name ):
        self.error_name = _error_name
