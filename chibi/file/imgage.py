from chibi.file import Chibi_file
from PIL import Image


class Chibi_image( Chibi_file ):
    @property
    def dimension( self ):
        return self._PIL.size

    @property
    def _PIL( self ):
        return Image.open( self.file_name )
