class Connections:
    def __init__( self ):
        self._kwargs = {}
        self._connections = {}

    def configure( self, **kw ):
        self._connections = kw

    def add( self, name, connection ):
        self._connections[ name ] = connection

    def get( self, alias='default' ):
        if not isinstance( alias, str ):
            raise TypeError(
                "unexpected type '{}' expected '{}'"
                    .format( type( alias ), str ) )

        try:
            return self._connections[ alias ]
        except KeyError:
            raise KeyError(
                "there is no connection with name {}".format( alias ) )

    def __getitem__( self, name ):
        return self.get( name )

    def __setitem__( self, name ):
        return self.add( name )
