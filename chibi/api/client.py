from .connection import Connections


class Client:
    def __init__( self, connection_name='default' ):
        self._connections = Connections()
        self._default_connection_name = connection_name

    def using( self, name ):
        self._connections[ name ]
        return self.__class__( name )
