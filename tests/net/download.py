from chibi.net import download
import tempfile, shutil
from unittest import TestCase
from chibi.file import exists


class Test_download_lenna( TestCase ):
    def setUp( self ):
        self.download_folder = tempfile.mkdtemp()
        self.lenna_url = (
            'https://upload.wikimedia.org/wikipedia/en/2/24/Lenna.png' )

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
