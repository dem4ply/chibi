import collections
from collections import defaultdict


def _wrap( val, klass=None ):
    if type( val ) == dict:
        if klass is None:
            return Chibi_atlas( val )
        else:
            return klass( val )
    return val


class Chibi_atlas:
    """
    Clase para crear dicionarios para que sus keys sean leibles como
    atributos de classes
    """
    def __init__( self, d=None, *args, **kw ):
        if d is None:
            d = dict( *args, **kw )
        super().__setattr__( '_d_', d )

    def __contains__( self, key ):
        return key in self._d_

    def __nonzero__( self ):
        return bool( self._d_ )

    __bool__ = __nonzero__

    def __dir__( self ):
        return list( self._d_.keys() )

    def __eq__( self, other ):
        if isinstance( other, Chibi_atlas ):
            return other._d_ == self._d_
        return other == self._d_

    def __ne__( self, other ):
        return not self == other

    def __repr__( self ):
        return repr( self._d_ )

    def __getstate__( self ):
        import pdb
        pdb.set_trace()
        return ( self._d_, )

    def __setstate__( self, state ):
        import pdb
        pdb.set_trace()
        super().__setattr__( '_d_', state[0] )

    def __getattr__( self, attr_name ):
        try:
            if attr_name == '_d_':
                return super().__getattribute__( '_d_' )
            return self.__getitem__( attr_name )
        except KeyError:
            try:
                return super().__getattribute__( attr_name )
            except AttributeError as e:
                raise

    def __delattr__( self, attr_name ):
        try:
            del self._d_[ attr_name ]
        except KeyError:
            try:
                super().__delattr__( name )
            except AttributeError as e:
                raise

    def __getitem__( self, key ):
        value = _wrap( self.__getattribute__( '_d_' )[ key ] )
        return value

    def __setitem__( self, key, value ):
        self._d_[ key ] = value

    def __delitem__( self, key ):
        del self._d_[ key ]

    def __setattr__( self, name, value ):
        if name == "_d_":
            super().__setattr__( '_d_', value )
        elif name in self._d_ or not hasattr( self.__class__, name ):
            self._d_[ name ] = value
        else:
            super().__setattr__( name, value )

    def __iter__( self ):
        return iter( self._d_ )

    def __len__( self ):
        return len( self._d_ )

    def keys( self ):
        return self._d_.keys()

    def values( self ):
        return self._d_.values()

    def items( self ):
        return self._d_.items()


class Chibi_atlas_ignore_case( Chibi_atlas ):
    def __init__( self, *args, **kw ):
        args_clean = []
        for a in args:
            if isinstance( a, dict ) or hasattr( a, 'items' ):
                args_clean.append( { k.lower(): v for k, v in a.items() } )
        kw = { k.lower(): v for k, v in kw.items() }
        super().__init__( *args_clean, **kw )

    def __getattr__( self, name ):
        name = name.lower()
        return super().__getattr__( name )

    def __getitem__( self, key ):
        key = key.lower()
        return super().__getitem__( key )

    def __setattr__( self, name, value ):
        name = name.lower()
        return super().__setattr__( name, value )

    def __setitem__( self, key, value ):
        key = key.lower()
        return super().__setitem__( key, value )


class Chibi_atlas_default( Chibi_atlas ):
    def __init__( self, _default_factory=None, *args, **kw ):
        #d = defaultdict( _default_factory, *args, **kw )
        super().__init__( *args, **kw )
        self._d_ = defaultdict( _default_factory, self._d_ )
        #self._default_factory = _default_factory

    """
    def __getitem__( self, key ):
        try:
            value = super().__getitem__( key )
        except KeyError:
            value = self._default_factory()
            self[ key ] = value
        return value
    """
