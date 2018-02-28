from chibi.file import mkdir, join, exists
from tests.snippet.files import Test_with_files


class Test_is_dir( Test_with_files ):
    def test_create_a_new_dir_and_that_exists_should_be_ok_in_default( self ):
        mkdir( self.dirs[0] )

    def test_create_a_new_dir_and_that_exists_should_be_should_raise( self ):
        with self.assertRaises( OSError ):
            mkdir( self.dirs[0], False )

    def test_if_the_directory_no_exists_should_create( self ):
        new_dir = join( self.dirs[0], 'asdf' )
        if exists( new_dir ):
            self.fail(
                "el directiorio {} ya existe usar"
                "otro nombre".format( new_dir ) )
        mkdir( new_dir )
        if not exists( new_dir ):
            self.fail(
                "no se creo el directorio {} ".format( new_dir ) )
