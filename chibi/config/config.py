import logging
from chibi.atlas import Chibi_atlas
from chibi.file import Chibi_path
from chibi.file.other import Chibi_json, Chibi_yaml, Chibi_python


logger = logging.getLogger( 'chibi.config.Configuration' )


__all__ = [ 'Configuration' ]


class Configuration( Chibi_atlas ):
    def __getitem__( self, name ):
        return super().__getitem__( name )

    def __setitem__( self, name, value ):
        return super().__setitem__( name, value )

    def load( self, path ):
        path = Chibi_path( path )
        with path as f:
            if isinstance( f, ( Chibi_json, Chibi_yaml ) ):
                for k, v in f.read().items():
                    self[ k ] = v
            elif isinstance( f, Chibi_python ):
                value = f.read()
                logger.info( "ejecutanto archivo python {f}" )
                logger.debug( value )
                exec( value )
            else:
                raise NotImplementedError(
                    "no esta implementado la carga de configuracion de los "
                    f"archivos {type(f)} de {f}" )
