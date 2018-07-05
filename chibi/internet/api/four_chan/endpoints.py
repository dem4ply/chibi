import datetime
from chibi.api import Endpoint
from chibi.internet.api.four_chan.responses import (
    Thread_list as Thread_list_response
)


class Thread_list( Endpoint ):
    def build_response( self, response ):
        return Thread_list_response(
            response, board=self.parameters[ 'board' ])


class Thread( Endpoint ):
    url = 'http://a.4cdn.org/{board}/thread/{thread_number}.json'

    def __init__( self, *args, thread_number, last_modified, **kw ):
        thread_number = int( thread_number )
        last_modified = datetime.datetime.fromtimestamp( last_modified )
        return super().__init__(
            *args, thread_number=thread_number,
            last_modified=last_modified, **kw )

    def __repr__( self ):
        return "Thread( url={}, last_modifed={})".format( self.format_url,
            self.parameters[ 'last_modified' ] )


threads = Thread_list( 'http://a.4cdn.org/{board}/threads.json' )
