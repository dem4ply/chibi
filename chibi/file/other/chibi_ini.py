import re

from chibi.atlas import Chibi_atlas
from chibi.file import Chibi_file
from chibi.snippet.iter import chunk_each


__all__ = [ 'Chibi_ini' ]


category_regex = re.compile( r"\[.*\]" )


def from_string( data ):
    result = Chibi_atlas()
    lines = filter( bool, data.split( '\n' ) )
    lines = filter( lambda x: not x.startswith( '#' ), lines )
    chunks = chunk_each( lines, lambda x: category_regex.match( x ) )
    for section in chunks:
        section_key = section[0][1:-1].strip()
        section_data = section[1:]
        section_dict = Chibi_atlas()
        for line in section_data:
            key, value = line.split( '=', 1 )
            key = key.strip()
            value = value.strip()
            section_dict[key] = value
        result[ section_key ] = section_dict
    return result


def to_string( data ):
    result = ''
    for k in data.keys():
        section = data[ k ]
        section_str = _transform_section( k, section )
        result += section_str
    return result


def _transform_section( name, section ):
    result = f"[{name}]\n"
    for k, v in section.items():
        if isinstance( v, list ):
            for inner in v:
                result += f"{k}={inner}\n"
        else:
            result += f"{k}={v}\n"
    return result


class Chibi_ini( Chibi_file ):
    def read( self ):
        data = super().read()
        result = from_string( data )
        return result

    def write( self, data ):
        result = to_string( data )
        super().write( result )
