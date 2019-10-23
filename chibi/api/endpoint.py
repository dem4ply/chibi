from urllib import parse
from chibi.request.response import Response

import requests

from chibi.atlas import Chibi_atlas_ignore_case
from collections.abc import Iterable


class Endpoint():
    url = None

    def __init__(
            self, url=None, proxy=None, host=None,
            schema=None, headers=None, **kw ):
        if url is None:
            self._url = self.url
        else:
            self._url = url

        if host is None:
            self._host = None
        else:
            self._host = host

        if headers is None:
            self._headers = None
        else:
            self._headers = headers

        if schema is None:
            self._schema = None
        else:
            self._schema = schema

        self.proxy = proxy
        self.parameters = kw

    @property
    def proxy( self ):
        if self._proxy is None:
            return None
        if any( v for v in self._proxy.values() ):
            return self._proxy
        else:
            return None

    @proxy.setter
    def proxy( self, value ):
        if value is None:
            self._proxy = None
        elif not isinstance( value, dict ):
            raise TypeError()
        else:
            self._proxy = value

    @property
    def assigned_url( self ):
        if self._url is not None:
            return self._url
        else:
            return self.url

    @property
    def format_url( self ):
        return self._url_format()

    def build_response( self, response, method=None ):
        return Response( response )

    def _url_format( self ):
        result = self._url.format( **self.parameters )
        if self._host:
            p = parse.urlparse( result )
            p = p._replace( netloc=self._host )
            result = parse.urlunparse( p )
        if self._schema:
            p = parse.urlparse( result )
            p = p._replace( scheme=self._schema )
            result = parse.urlunparse( p )
        return result

    def format( self, **kw ):
        return self.__class__(
            self.assigned_url, proxy=self.proxy, host=self._host,
            headers=self._headers, **kw )

    def __copy__( self ):
        return self.__class__( **vars( self ) )

    def __dict__( self ):
        result = {
            'url': self._url, 'proxy': self.proxy, 'host': self._host,
            'headers': self._headers, 'schema': self._schema }
        result.update( self.parameters )
        return result


class GET:
    def get( self, **kw ):
        response = requests.get(
            self.format_url, proxies=self.proxy, headers=self._headers,
            params=kw )
        return self.build_response( response, method='get' )


class GET_plain_list( GET ):
    def get( self, **kw ):
        kw_end = {}
        for k, v in kw.items():
            if isinstance( v, Iterable ):
                kw_end[ k ] = ",".join( str( i ) for i in v )
            else:
                kw_end[ k ] = v
        return super().get( **kw_end )


class POST:
    def generate_post_headers( self ):
        return self._headers

    @property
    def is_json( self ):
        headers = self.generate_post_headers()
        if headers:
            return headers.get( 'Content-Type', None ) == 'application/json'
        else:
            return False

    def post( self, body=None ):
        headers = self.generate_post_headers()
        if self.is_json:
            response = requests.post(
                self.format_url, json=body, headers=headers,
                proxies=self.proxy )
        else:
            response = requests.post(
                self.format_url, data=body, headers=headers,
                proxies=self.proxy )
        return self.build_response( response, method='post' )
