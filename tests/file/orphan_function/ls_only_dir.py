from tests.snippet.files import Test_with_files
from chibi.file import ls_only_dir, is_dir


class Test_ls_only_dir( Test_with_files ):
    def test_should_list_all_dirs_and_not_the_files_from_root( self ):
        result = ls_only_dir( self.root_dir )
        for dir in result:
            self.assertTrue( is_dir( result ) )

    def test_should_return_a_empty_list( self ):
        result = list( ls_only_dir( self.empty_folder ) )
        self.assertFalse( result )
