from chibi.file import Chibi_path
from tests.snippet.files import Test_with_files


class Test_chibi_file_symbolic_linkx( Test_with_files ):
    def setUp( self ):
        super().setUp()
        self.chibi_path = self.files_with_content[0]

    def test_create_a_new_symbolic_link( self ):
        link_target = self.chibi_path.dir_name + 'asdf'
        self.assertFalse( link_target.exists )
        new_link = self.chibi_path.link( link_target )
        self.assertEqual( new_link, link_target )
        self.assertTrue( new_link.properties.is_link )
        self.assertEqual( new_link.properties.link_target, self.chibi_path )

    def test_create_a_new_symbolic_link_with_relative_path( self ):
        link_target = Chibi_path( '__delete__me__i_am_a_test__' )
        self.assertFalse( link_target.exists )
        new_link = self.chibi_path.link( link_target )
        self.assertEqual( new_link, link_target )
        self.assertTrue( new_link.properties.is_link )
        self.assertEqual( new_link.properties.link_target, self.chibi_path )
        link_target.delete()
