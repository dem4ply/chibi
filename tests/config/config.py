import unittest
from tests.snippet.files import Test_with_files
from chibi import config


class Test_load_config( Test_with_files ):
    def test_should_load_the_settings_from_a_pyton_file( self ):
        python_file = self.root_dir.temp_file( extension='py' )
        self.assertNotIn( 'hello', config.configuration  )
        with python_file as f:
            f.append( 'from chibi.config import configuration\n' )
            f.append( 'configuration.hello = "asdf"' )

        config.load( python_file )
        self.assertEqual( config.configuration.hello, 'asdf' )

    def test_when_read_a_json_should_put_all_the_content_in_the_config( self ):
        json_file = self.root_dir.temp_file( extension='json' )
        self.assertNotIn( 'json_hello', config.configuration  )
        with json_file as f:
            f.write( { 'json_hello': '1234567890' } )

        config.load( json_file )
        self.assertEqual( config.configuration.json_hello, '1234567890' )


    def test_when_read_a_yaml_should_put_all_the_content_in_the_config( self ):
        yaml_file = self.root_dir.temp_file( extension='yaml' )
        self.assertNotIn( 'yaml_hello', config.configuration  )
        with yaml_file as f:
            f.write( { 'yaml_hello': 'qwertyuiop' } )

        config.load( yaml_file )
        self.assertEqual( config.configuration.yaml_hello, 'qwertyuiop' )
