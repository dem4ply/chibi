from unittest import TestCase
from chibi.file.temp import Chibi_temp_path
from chibi.file.other import Chibi_csv


class Test_chibi_csv( TestCase ):
    def setUp( self ):
        self.folder = Chibi_temp_path()
        self.file_csv = self.folder.temp_file( extension='csv' )

    def test_should_append_the_range( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        csv.append( range( 10 ) )
        result = list( csv.read_as_list() )
        self.assertTrue( result )
        self.assertEqual( len( result ), 4 )

    def test_should_append_dicts( self ):
        csv = Chibi_csv( self.file_csv )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9', 'cosa4': 'a' } )
        csv.append( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' } )
        result = list( csv.read_as_dict() )
        self.assertEqual( len( result ), 3 )
        for r in result:
            self.assertIsInstance( r, dict  )
            self.assertTrue( r )
            self.assertEqual( { 'cosa1': '1', 'cosa2': '3', 'cosa3': '9' }, r )
