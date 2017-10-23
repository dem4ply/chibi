class Chibi_atlas( dict ):
    """
    Clase para crear dicionarios para que sus keys sean leibles como
    atributos de classes
    """
    def __getattr__( self, name ):
        try:
            return self[ name ]
        except KeyError as e:
            try:
                return super().__getattr__( name )
            except AttributeError as e:
                raise

    def __setattr__( self, name, value ):
        self[ name ] = value
