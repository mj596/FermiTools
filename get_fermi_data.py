
MIN_E = 40.
MAX_E = 300000.

from optparse import OptionParser

parser = OptionParser( )
parser.add_option("--source", dest="source", default='None',
                  help="source name" )
parser.add_option("--ra", dest="ra",
                  help="RA [deg]" )
parser.add_option("--dec", dest="dec",
                  help="DEC [deg]" )
parser.add_option("--time-format", dest="time_format", default='MET',
                  help="time_format: ISO or MET" )
parser.add_option("--tstart", dest="time_start", default=0.,
                  help="start time in choosen format" )
parser.add_option("--tstop", dest="time_stop", default=0.,
                  help="end time in choosen format" )
parser.add_option("--emin", dest="energy_min", default='100.',
                  help="minimal energy in MeV" )
parser.add_option("--emax", dest="energy_max", default='300000.',
                  help="maximal energy in MeV" )
parser.add_option("--roi", dest="roi", default='10.',
                  help="ROI in degrees" )
parser.add_option("--dir", dest="dir", default='downloaded',
                  help="download directory" )

(options, args) = parser.parse_args()

import sys
if len(sys.argv) <= 1:
    parser.print_help( )
    sys.exit( )

# if you uncomment this you get optparse data formatted with tabulate
# def optparse_to_array( input ):
#     table = []
#     for opt, value in input.__dict__.items():
#         table.append( [ opt, value ] )
# 
#     return table
# 
# from tabulate import tabulate
# print( "Let\'s try to download Fermi data for these settings\n" )
# print( tabulate( optparse_to_array( options ), headers=[ 'Parameter', 'Value' ] ) )

def check_energy_range( emin, emax ):
    if emin < MIN_E:
        raise ValueError( 'E min must be >= 30 MeV' )
    elif emax > MAX_E:
        raise ValueError( 'E max must be <= 300 000 MeV' )
    elif emax <= emin:
        raise ValueError( 'E max must be > E min' )


# initialize time converter
import modules.iso8601time.iso8601time as iso8601time
time_converter = iso8601time.TimeConverter( )
time_converter.set_mission( 'Fermi' )

# MET=0 for Fermi
TSTART_MET = 239557417.
# current time -3 days for safety
TSTOP_MET = float( time_converter.get_current_time( )-3*24*3600 ) 
TSTART_ISO = time_converter.convert_seconds_to_iso( TSTART_MET )
TSTOP_ISO = time_converter.convert_seconds_to_iso( TSTOP_MET )

# set time_start and time_stop in current time format
def set_time( ):
    if options.time_start == 0.:
        if options.time_format == 'ISO':
            time_start = TSTART_ISO
        elif options.time_format == 'MET':
            time_start = TSTART_MET
        else:
            raise ValueError( 'ERROR Unrecognized time format' )
    else:
        time_start = options.time_start

    if options.time_stop == 0.:
        if options.time_format == 'ISO':
            time_stop = TSTOP_ISO
        elif options.time_format == 'MET':
            time_stop = TSTOP_MET
        else:
            raise ValueError( 'ERROR Unrecognized time format' )
    else:
        time_stop = options.time_stop

    return ( time_start, time_stop )

# check and recalculate time
def check_and_recalculate_time( tstart, tstop ):
    if options.time_format == 'MET':
        time_start_met = time_start
        time_stop_met = time_stop
        time_start_iso = time_converter.convert_seconds_to_iso( time_start_met )
        time_stop_iso = time_converter.convert_seconds_to_iso( time_stop_met )
    elif options.time_format == 'ISO':
        time_start_iso = time_start
        time_stop_iso = time_stop
        time_start_met = time_converter.convert_iso_to_seconds( time_start_iso )
        time_stop_met = time_converter.convert_iso_to_seconds( time_stop_iso )
    else:
        raise ValueError( 'ERROR Unrecognized time format' )

    if float(time_start_met) < float(TSTART_MET):
        raise ValueError( 'Start time is before Fermi started taking data' )
    elif float(time_start_met) >= float(time_stop_met):
        raise ValueError( 'Start time >= stop time' )
    elif float(time_stop_met) > float(TSTOP_MET): # TSTOP_MET +1 day for safety
        raise ValueError( 'Stop time is yet to come' )

    return ( time_start_met, time_stop_met, time_start_iso, time_stop_iso )

try:
    check_energy_range( float(options.energy_min), float(options.energy_max) )
    ( time_start, time_stop ) = set_time( )
    ( time_start_met, time_stop_met, time_start_iso, time_stop_iso ) = check_and_recalculate_time( time_start, time_stop  )
except ValueError as error:
    print( 'ERROR ' + str(error) )
    sys.exit( )

print( "\n" )
print( "Let\'s try to download Fermi data for these settings" )
print( 'source \t %s' % ( options.source ) )
print( 'RA \t %s deg' % ( options.ra ) )
print( 'DEC \t %s deg' % ( options.dec ) )
print( 'min energy \t %s MeV' % ( options.energy_min ) )
print( 'max energy \t %s MeV' % ( options.energy_max ) )
print( 'time format \t %s' % ( options.time_format ) )
print( 'time start \t %s (MET) - %s (ISO)' % ( time_start_met, time_start_iso ) )
print( 'time stop \t %s (MET) - %s (ISO)' % ( time_stop_met, time_stop_iso ) )
print( 'ROI \t %s' % ( options.roi ) )
print( "\n" )

# get rid of UserWarning when importing fermi downloader
import warnings
warnings.filterwarnings('ignore', '.*fermi.*',)

# initialize Fermi downloader
import modules.fermi_downloader.fermi_downloader as fermi_downloader
fermi_data = fermi_downloader.FermiData( )

# set Fermi download data
fermi_data.set_coords( options.ra, options.dec )
fermi_data.set_time( float(time_start_met), float(time_stop_met) )
fermi_data.set_energy( options.energy_min, options.energy_max )
fermi_data.set_roi( options.roi )

# get links
fermi_data.get_data( )
 
print( 'Files to download: ' )
for item in fermi_data.get_files_to_download( ):
     print( item )
 
print( '... and a webpage with results:' )
webpage = fermi_data.get_download_webpage( )
print( webpage )

import os
download_dir = str( options.dir )
if os.path.exists( download_dir ):
    print( 'Download destination `%s` does exist. Please remove first. I will nor overwrite it!' % (download_dir) )
    sys.exit( )
else:
    print( 'Creating directory \'%s\'' % (download_dir) )
    os.mkdir( download_dir )

# use urlgrabber to download files with progressbar
import urlgrabber, re
import urlgrabber.progress

print( '\nDownloading ... ' )
for file in fermi_data.get_files_to_download( ):
    file_name = file.split('/')[-1]
    prog = urlgrabber.progress.text_progress_meter( )
    urlgrabber.urlgrab( file, options.dir + '/' + file_name, progress_obj=prog )
print( 'Done' )

# save some info about downloaded data
import time
file = open( options.dir + '/downloaded.info', 'w' )
file.write( 'Created on %s\n' % ( time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) ) )
file.write( 'source \t %s\n' % ( options.source ) )
file.write( 'RA \t %s deg\n' % ( options.ra ) )
file.write( 'DEC \t %s deg\n' % ( options.dec ) )
file.write( 'min energy \t %s MeV\n' % ( options.energy_min ) )
file.write( 'max energy \t %s MeV\n' % ( options.energy_max ) )
file.write( 'time format \t %s\n' % ( options.time_format ) )
file.write( 'time start \t %s (MET) - %s (ISO)\n' % ( time_start_met, time_start_iso ) )
file.write( 'time stop \t %s (MET) - %s (ISO)\n' % ( time_stop_met, time_stop_iso ) )
file.write( 'ROI \t %s\n' % ( options.roi ) )

# save filelist
file = open( options.dir + '/' + options.source + '.filelist', 'w' )

for filename in fermi_data.get_files_to_download( ):
    file_name = filename.split('/')[-1]
    if not 'SC' in file_name:
        file.write( options.dir + '/' + file_name )
    else:
        SCfile = options.dir + '/' + file_name

print( '\nPH files list: %s' % ( options.dir + '/' + options.source + '.filelist' ) )
print( 'SC file: %s' % ( SCfile ) )
