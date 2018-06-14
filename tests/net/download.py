import tempfile, shutil

from chibi.file import exists
from chibi.net import download
from unittest import TestCase


class Test_download_lenna( TestCase ):
    def setUp( self ):
        self.download_folder = tempfile.mkdtemp()
        self.lenna_url = (
            'http://www.lenna.org/len_std.jpg' )

    def tearDown(self):
        shutil.rmtree( self.download_folder )

    def test_download_lenna( self ):
        lenna = download( self.lenna_url, directory=self.download_folder )
        self.assertTrue( exists( lenna ) )

    def test_download_wiith_file_name( self ):
        lenna = download(
            self.lenna_url, directory=self.download_folder,
            file_name='helloooo_lenna.png' )
        self.assertTrue( lenna.endswith( 'helloooo_lenna.png' ) )
        self.assertTrue( exists( lenna ) )