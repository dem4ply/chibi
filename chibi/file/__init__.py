import mmap
import os
import shutil
import hashlib
from pwd import getpwnam, getpwuid
from grp import getgrgid, getgrnam
from chibi.atlas import Chibi_atlas
from chibi.nix import get_passwd, get_group
from chibi import chibi_base64


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
    return ( name for name in ls( src ) if is_dir( join( src, name ) ) )


def mkdir( new_dir, is_ok_exists=True, verbose=True):
    """
    crea un nuevo directiorio

    Parameters
    ==========
    new_dir: string
        nombre o direcion del nuevo directorio
    is_ok_exists: bool
        define si esta bien is el directorio ya existe
        y no lanza una exception
    """
    try:
        os.makedirs( inflate_dir( new_dir ), )
        if verbose:
            print( "se creo el directorio '{}'".format( new_dir ) )
    except OSError:
        if not is_ok_exists:
            raise


def join( *patch ):
    """
    une los argumentes en una direcion

    Parameters
    ==========
    patch: list of strings

    Returns
    =======
    string
    """
    return os.path.join( *patch )


def exists( file_name ):
    """
    revisa si el archivo existe en la ruta

    Parameters
    ==========
    file_name: string

    Returns
    =======
    bool
    """
    return os.path.exists( file_name )


def copy( source, dest, verbose=False ):
    """
    copia el contenido de un archivo al destino

    Parameters
    ==========
    source: string
        ruta del archivo original
    dest: string
        ruta del destine del nuevo archivo
    verbose: bool

    Returns
    =======
    None
    """
    shutil.copy( source, dest )
    if verbose:
        print( source, '->', dest )


def ln( source, dest, verbose=True ):
    os.symlink( source, dest )
    if verbose:
        print( source, '->', dest )


def _print_verboce_chown( path, old_stat, current_stat ):
    user_change = old_stat.user.name != current_stat.user.name
    group_change = old_stat.group.name != current_stat.group.name

    if user_change or group_change:
        print(
            "el propietario de '{path}' cambio de '{old}' a '{new}'"
            .format(
                path=path, new="{user}:{group}".format(
                    user=current_stat.user.name,
                    group=current_stat.group.name ),
                old="{user}:{group}".format(
                    user=old_stat.user.name, group=old_stat.group.name ) ) )
    else:
        print(
            "el propietario de '{path}' permanece '{old}'"
            .format(
                path=path, new="{user}:{group}".format(
                    user=current_stat.user.name,
                    group=current_stat.group.name ),
                old="{user}:{group}".format(
                    user=old_stat.user.name, group=old_stat.group.name ) ) )


def read_in_chunks( file_name, prop='rb', chunk_size=4096 ):
    with open( file_name, prop ) as f:
        while True:
            current_read = f.read( chunk_size )
            if not current_read:
                break
            yield current_read


def check_sum_md5( file_name, check_sum ):
    md5 = hashlib.md5()
    for chunk in read_in_chunks( file_name ):
        md5.update( chunk )
    md5_bin = md5.digest()
    return chibi_base64.encode( md5_bin ) == check_sum


def delete( path ):
    if is_file( path ):
        os.remove( path )
    else:
        shutil.rmtree( path )


def chown(
        *paths, verbose=True, user_name=None, group_name=None,
        recursive=False ):
    if user_name is None:
        user = None
        uid = -1
    else:
        user = get_passwd( name=user_name )
        uid = user.uid

    if group_name is None:
        group = None
        gid = -1
    else:
        group = get_group( name=group_name )
        gid = group.gid

    for path in paths:
        old_stat = stat( path )
        os.chown( path, uid, gid )
        current_stat = stat( path )
        if verbose:
            _print_verboce_chown( path, old_stat, current_stat )

        if recursive and is_dir( path ):
            inner_paths = (
                join( path, dir )
                for dir in ls( inflate_dir( path ) ) )
            chown(
                *inner_paths, user=user, group=group, verbose=verbose,
                recursive=True )


def stat( src ):
    s = os.stat( src )
    result = Chibi_atlas( dict( mode=s.st_mode, ino=s.st_ino, dev=s.st_dev,
        nlink=s.st_nlink, size=s.st_size, atime=s.st_atime, mtime=s.st_mtime,
        ctime=s.st_ctime ) )
    result.user = get_passwd( uid=s.st_uid )
    result.group = get_group( gid=s.st_gid )

    return result



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
        try:
            self._file_content.close()
        except AttributeError:
            pass

    def find( self, string_to_find ):
        if isinstance( string_to_find, str ):
            string_to_find = string_to_find.encode()
        return self._file_content.find( string_to_find )

    def reread( self ):
        try:
            with open( self._file_name, 'r' ) as f:
                self._file_content = mmap.mmap(
                    f.fileno(), 0, prot=mmap.PROT_READ )
        except ValueError as e:
            if not str( e ) == 'cannot mmap an empty file':
                raise

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

    @property
    def properties( self ):
        raise NotImplementedError

    def chunk( self, chunk_size=4096 ):
        return read_in_chunks( self.file_name, 'r', chunk_size=chunk_size )

    def check_sum_md5( self, check_sum ):
        return check_sum_md5( self.file_name, check_sum )
