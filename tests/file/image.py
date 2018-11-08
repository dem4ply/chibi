from unittest import TestCase

from chibi.file.imgage import Chibi_image


class Test_imges( TestCase ):
    def setUp( self ):
        self.jpg_path = './tests/file/1529990793499.jpg'
        self.png_path = './tests/file/1535359854403.png'
        self.gif_path = './tests/file/1536637012160.gif'

        self.jpg = Chibi_image( self.jpg_path )
        self.png = Chibi_image( self.png_path )
        self.gif = Chibi_image( self.gif_path )

    def test_can_open_the_images( self ):
        self.assertTrue( self.jpg.exists )
        self.assertTrue( self.png.exists )
        self.assertTrue( self.gif.exists )

        self.assertFalse( self.jpg.is_empty )
        self.assertFalse( self.png.is_empty )
        self.assertFalse( self.gif.is_empty )
