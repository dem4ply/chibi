from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi.file.other.simple_env import Chibi_conf_env
from chibi_atlas import Chibi_atlas


content = """
user = apache
group = apache
IP=192.168.1.5
MASK=24
"""


class Test_chibi_simple_env_conf( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file_service = self.folder.temp_file( extension='conf' )
        with open( self.file_service, 'w' ) as f:
            f.write( content )

    def test_should_be_a_dict( self ):
        conf = Chibi_conf_env( self.file_service )
        result = conf.read()
        self.assertIsInstance( result, Chibi_atlas )

    def test_should_have_expected_data( self ):
        conf = Chibi_conf_env( self.file_service )
        result = conf.read()
        expected = {
            'user': 'apache',
            'group': 'apache',
            'IP': '192.168.1.5',
            'MASK': '24',
        }
        self.assertEqual( result, expected )

    def test_when_change_variable_should_work( self ):
        conf = Chibi_conf_env( self.file_service )
        result = conf.read()
        result[ 'user' ] = 'qwert'
        conf.write( result )
        result_2 = conf.read()
        expected = {
            'user': 'qwert',
            'group': 'apache',
            'IP': '192.168.1.5',
            'MASK': '24',
        }
        self.assertEqual( result_2, expected )
