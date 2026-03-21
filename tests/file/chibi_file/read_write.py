from tests.snippet.files import Test_with_files
import json
from chibi.file import Chibi_file


class Test_chibi_file_text( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.file_path = self.root_dir.temp_file( extension='json' )
        self.chibi_file = Chibi_file( self.file_path )
        self.data = { 'a': 'a' }
        self.json_data = json.dumps( self.data )
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertFalse( whole_file, "el archivo no esta vacio" )
        self.chibi_file.write( self.data )
        whole_file = "".join( self.chibi_file.chunk() )
        self.assertEqual( whole_file, self.json_data )

    def test_read_text_should_return_str( self ):
        result = self.chibi_file.read_text()
        self.assertIsInstance( result, str )
        self.assertTrue( result )
        data = json.loads( result )
        self.assertEqual( data, self.data )

    def test_write_text_should_return_overwrite_file( self ):
        expected = "hello my world!!!"
        self.chibi_file.write_text( expected )
        result = self.chibi_file.read_text()

        self.assertIsInstance( result, str )
        self.assertEqual( result, expected )
