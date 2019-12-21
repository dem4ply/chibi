import yaml
from chibi.file import Chibi_file


__all__ = [ 'Chibi_yaml' ]


class Chibi_yaml( Chibi_file ):
    def read( self ):
        self.reread()
        result = yaml.load( self.file, Loader=yaml.FullLoader )
        return _wrap( result )

    def write( self, data, is_safe=False ):
        if is_safe:
            self.write( yaml.safe_dump( data ) )
        else:
            self.write( yaml.dump( data ) )
