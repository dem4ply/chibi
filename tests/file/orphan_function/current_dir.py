from unittest import TestCase
from chibi.file import current_dir, cd


class Test_current_dir( TestCase ):
    def move_root( self ):
        cd( '/' )

    def move_home( self ):
        cd( '~' )

    def test_current_dir_should_return_a_string( self ):
        result = current_dir()
        self.assertIsInstance( result, str )

    def test_current_dir_should_no_return_empty( self ):
        result = current_dir()
        self.assertTrue( result )

    def test_current_dir_is_different_when_move_to_home( self ):
        first_current_dir = current_dir()
        self.move_home()
        home_dir = current_dir()
        self.assertNotEqual( first_current_dir, home_dir )

    def test_current_dir_is_different_when_move_to_root( self ):
        first_current_dir = current_dir()
        self.move_root()
        root_dir = current_dir()
        self.assertNotEqual( first_current_dir, root_dir )
