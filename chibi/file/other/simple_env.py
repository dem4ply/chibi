import re

from chibi.atlas import Chibi_atlas
from chibi_atlas.multi import Chibi_atlas_multi
from chibi.file import Chibi_file
from chibi.snippet.iter import chunk_each


__all__ = [ 'Chibi_conf_env' ]


category_regex = re.compile( r"\[.*\]" )


class Chibi_conf_env( Chibi_file ):
    """
    chibi file para leer y escribir archivos de tipo .env o configuracion
    sensilla

    Examples
    --------
    >>>f = Chibi_conf_env( "/tmp/file.conf" )
    >>>f.write( { 'key': 'value', 'key2': 'value2' } )
    >>>f.read_text()
    key=value
    key2=value2
    """
    def read( self ):
        text = self.read_text()
        data = from_string( text )
        return data

    def write( self, data ):
        result = to_string( data )
        super().write_text( result )


def from_string( text ):
    lines = text.split( '\n' )
    lines = filter( bool, lines )
    lines = ( l.split( '=', 1 ) for l in lines )
    lines = ( ( k.strip(), v.strip() ) for k, v in lines )
    result = Chibi_atlas( dict( lines ) )
    return result


def to_string( data ):
    result = ( f"{k}={v}" for k, v in data.items() )
    result = "\n".join( result )
    return result
