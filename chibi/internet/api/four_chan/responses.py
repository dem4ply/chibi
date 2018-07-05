from chibi.api.endpoint import Response
from functools import reduce


class Thread_list( Response ):
    def __init__( self, *args, board, **kw ):
        super().__init__( *args, **kw )
        self.board = board


    @property
    def native( self ):
        try:
            return self._native
        except AttributeError:
            from chibi.internet.api.four_chan.endpoints import Thread
            raw_list = self._response.json()
            threads = reduce(
                ( lambda x, y: x + y ),
                ( page[ 'threads' ] for page in raw_list ) )

            self._native = [
                Thread(
                    board=self.board, thread_number=t[ 'no' ],
                    last_modified=t[ 'last_modified' ] )
                for t in threads ]
            return self._native
