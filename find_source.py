from optparse import OptionParser

parser = OptionParser( )
parser.add_option("--source", dest="source", default='None',
                  help="specify target to search in online database" )
parser.add_option("--database", dest="database", default='NED',
                  help="specify online database: NED, Simbad, Vizier" )

(options, args) = parser.parse_args()

import sys
if len(sys.argv) <= 1:
    parser.print_help( )
    sys.exit( )

from modules.search_source import SearchSource
source = SearchSource( )

source.set_source( options.source )
source.set_db( options.database )

( name, ra, dec ) = source.get_source_info( )

print( 'Requested source name: %s\nFound source name: %s\nRA: %s\nDEC: %s\n' % ( options.source, name, ra, dec ) )
print( 'In case you want to use it with \'get_fermi_data.py\'\n\t--source=%s --ra=%s --dec=%s' % ( options.source, ra, dec) )
