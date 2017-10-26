import mmap
import os
import shutil


def current_dir():
    """
    regresa el directorio actual de trabajo

    Returns
    =======
    string
    """
    return os.getcwd()


def cd( to ):
    """
    cambia el directorio actual

    Parameters
    ==========
    to: string
        dirrecion a la que se quiere cambiar

    Returns
    =======
    None
    """
    to = inflate_dir( to )
    os.chdir( to )


def inflate_dir( src ):
    """
    infla la dirrecion para obtner la ruta absoluta

    Parameters
    ==========
    src: string
        direcion que se quiere inflar

    Returns
    =======
    string
    """
    if '~' in src:
        return os.path.expanduser( src )
    else:
        return os.path.abspath( src )


def is_dir( src ):
    """
    revisa si una direcion es un directorio

    Returns
    =======
    bool
    """
    return os.path.isdir( src )


def is_file( src ):
    """
    revisa si una direcion es un archivo

    Returns
    =======
    bool
    """
    return os.path.isfile( src )


def ls( src=None ):
    """
    lo mismo que ls en unix

    Returns
    =======
    iterador of strings
    """
    if src is None:
        src = current_dir()
    return ( name for name in os.listdir( src ) )


def ls_only_dir( src=None ):
    """
    lo mismo que ls en unix

    Returns
    =======
    iterador of strings
    """
    return ( name for name in ls( src ) if is_dir( name ) )


def join( *patch ):
    return os.path.join( *patch )


def exists( file_name ):
    return os.path.exists( file_name )


def copy( source, dest ):
    shutil.copy( source, dest )


class Chibi_file:
    def __init__( self, file_name ):
        self._file_name = file_name
        if not self.exists:
            self.touch()
        self.reread()

    @property
    def file_name( self ):
        return self._file_name

    def __del__( self ):
        self._file_content.close()

    def find( self, string_to_find ):
        if isinstance( string_to_find, str ):
            string_to_find = string_to_find.encode()
        return self._file_content.find( string_to_find )

    def reread( self ):
        with open( self._file_name, 'r' ) as f:
            self._file_content = mmap.mmap( f.fileno(), 0,
                                            prot=mmap.PROT_READ )

    def __contains__( self, string ):
        return self.find( string ) >= 0

    def append( self, string ):
        with open( self._file_name, 'a' ) as f:
            f.write( string )
        self.reread()

    @property
    def exists( self ):
        return exists( self.file_name )

    def touch( self ):
        open( self.file_name, 'a' ).close()

    def copy( self, dest ):
        copy( self.file_name, dest )
