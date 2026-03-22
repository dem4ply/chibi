from chibi.file.snippets import stat
from tests.snippet.files import Test_with_files


class Test_stat_to_dir( Test_with_files ):
    amount_of_files = 3
    amount_of_dirs = 3

    def test_stat_to_dir_should_no_raise_a_exception( self ):
        stat( self.root_dir )

    def test_stat_to_dir_should_return_the_group( self ):
        result = stat( self.root_dir )
        self.assertIn( 'group', result )

    def test_stat_to_dir_should_return_the_user( self ):
        result = stat( self.root_dir )
        self.assertIn( 'user', result )


class Test_stat_to_file( Test_with_files ):
    amount_of_files = 3
    amount_of_dirs = 3

    def test_stat_to_file_should_no_raise_a_exception( self ):
        stat( self.files[0] )

    def test_stat_to_file_should_return_the_group( self ):
        result = stat( self.files[0] )
        self.assertIn( 'group', result )

    def test_stat_to_file_should_return_the_user( self ):
        result = stat( self.files[0] )
        self.assertIn( 'user', result )

    def test_stat_should_have_is_a_link( self ):
        result = stat( self.files[0] )
        self.assertIn( 'is_link', result )
        self.assertFalse( result[ 'is_link' ] )
