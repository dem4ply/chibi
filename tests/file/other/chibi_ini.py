from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi.file.other import Chibi_ini


content = """
[LightDM]
#log-directory=/var/log/lightdm
run-directory=/run/lightdm
#cache-directory=/var/cache/lightdm

#
# Seat configuration
#
# Seat configuration is matched against the seat name glob
# in the section, for example:
# [Seat:*] matches all seats and is applied first.
# [Seat:seat0] matches the seat named "seat0".
# [Seat:seat-thin-client*] matches all seats that
# have names that start with "seat-thin-client".
#
#
[Seat:*]
#type=local
#allow-user-switching=true
#allow-guest=true
#guest-session=
session-wrapper=/etc/lightdm/Xsession
#greeter-wrapper=
#guest-wrapper=
#exit-on-failure=false
"""


class Test_chibi_ini( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file = self.folder.temp_file( extension='ini' )
        self.file.open().write( content )

    def test_should_be_a_dict( self ):
        service = Chibi_ini( self.file )
        result = service.read()
        self.assertIsInstance( result, dict )

    def test_should_have_the_2_sections( self ):
        service = Chibi_ini( self.file )
        result = service.read()
        self.assertIn( 'LightDM', result )
        self.assertIn( 'Seat:*', result )

    def test_read_should_be_the_expected( self ):
        service = Chibi_ini( self.file )
        result = service.read()
        expected = {
            'LightDM': {
                'run-directory': '/run/lightdm'
            },
            'Seat:*': {
                'session-wrapper': '/etc/lightdm/Xsession'
            }
        }
        self.assertEqual( result, expected )

    def test_write_should_write_update_the_file_using_ini_format( self ):
        service = Chibi_ini( self.file )
        result = service.read()
        result.LightDM[ 'cache-directory' ] = '/var/cache/lightdm'
        service.write( result )
        result_after_save = service.read()
        self.assertEqual( result, result_after_save )
