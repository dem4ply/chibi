import logging
import os

import chibi_donkey as donkey

from chibi.atlas import Chibi_atlas, Chibi_atlas_default, Atlas
from chibi.file import Chibi_path
from chibi.file.other import Chibi_json, Chibi_yaml, Chibi_python
from chibi.config.exception import Chibi_config_not_set


logger = logging.getLogger( 'chibi.config.Configuration' )


__all__ = [ 'Configuration' ]


def _default_factory():
    return Configuration()


class Configuration( Chibi_atlas_default ):
    """
    esta clase funciona como un simple dicionario de atributos para asignar
    configuraciones
    """
    def __init__( self, default_factory=None, *args, _path='', **kw ):
        if default_factory is None:
            default_factory = _default_factory
        super().__init__( default_factory, *args, **kw )
        object.__setattr__( self, '_path', _path )

    def __missing__( self, key ):
        if self._path:
            child_path = f"{self._path}.{key}"
        else:
            child_path = key
        value = self.default_factory()
        if isinstance( value, Configuration ):
            object.__setattr__( value, '_path', child_path )
        self[ key ] = value
        return value

    def required( self, path=None ):
        """
        resuelve un path de puntos y valida que el valor final no
        este vacio

        Parameters
        ----------
        path: str
            ruta separada por puntos, ej 'api.host'

        Raises
        ------
        Chibi_config_not_set
            si el valor resuelto es falso

        Examples
        --------
        >>> configuration.api.host = 'localhost'
        >>> configuration.require( 'api.host' )
        'localhost'
        >>> configuration.api.require( 'api.host' )
        'localhost'
        """
        if path is None:
            if not self:
                raise Chibi_config_not_set( self._path )
            return self

        value = self
        for part in path.split( '.' ):
            if not isinstance( value, Configuration ):
                value = value[ part ]
            else:
                value = getattr( value, part )

        if self._path:
            full_path = f"{self._path}.{path}"
        else:
            full_path = path

        if not value:
            raise Chibi_config_not_set( full_path )
        return value

    def load( self, path ):
        path = Chibi_path( path )
        with path as f:
            if isinstance( f, ( Chibi_json, Chibi_yaml ) ):
                for k, v in f.read().items():
                    self[ k ] = v
            elif isinstance( f, Chibi_python ):
                logger.info( f"ejecutanto archivo python {f}" )
                f.import_()
            else:
                raise NotImplementedError(
                    "no esta implementado la carga de configuracion de los "
                    f"archivos {type(f)} de {f}" )


class Logger_configuration( Chibi_atlas ):
    """
    su default busca los loggers de python usnado el key
    """
    def __getitem__( self, name ):
        try:
            return super().__getitem__( name )
        except KeyError:
            # logger = logging.getLogger( name )
            self[ name ] = Logger( name=name )
            return super().__getitem__( name )


class Logger( Chibi_atlas ):
    @property
    def level( self ):
        logger = self.logger
        while logger:
            if logger.level != logging.NOTSET:
                return logger.level
            logger = logger.parent
        return self.logger.level

    @level.setter
    def level( self, value ):
        if isinstance( value, str ):
            level = getattr( logging, value )
            if isinstance( level, int ):
                self.logger.setLevel( level )
            else:
                raise NotImplementedError(
                    f"no esta implementado la asignacion del level de {value}"
                )
        elif isinstance( value, int ):
            self.logger.setLevel( value )
        else:
            raise NotImplementedError(
                f"no esta implementado la asignacion del level de {value}" )

    @property
    def logger( self ):
        return logging.getLogger( self.name )


class Env_vars( Configuration ):
    def __init__( self, default_factory=None, *args, **kw ):
        if default_factory is None:
            default_factory = str
        d = Atlas( donkey.inflate( os.environ ) )
        super().__init__( default_factory, d, *args, **kw )
