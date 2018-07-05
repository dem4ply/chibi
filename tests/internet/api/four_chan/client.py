import datetime
from unittest import TestCase, skip
from chibi.internet.api.four_chan.client import Board
from chibi.internet.api.four_chan.endpoints import Thread
from chibi.internet.api.four_chan import w, wallpaper


class Test_board_wallpaper( TestCase ):
    def setUp( self ):
        self.w = w


class Test_threads( Test_board_wallpaper ):
    def test_endpoint_for_threads_should_point_to_wallpapers( self ):
        self.assertEqual(
            self.w.thread_endpoint.assigned_url,
            'http://a.4cdn.org/w/threads.json' )

    def test_should_get_threads_from_wallpapers( self ):
        response = self.w.threads()
        self.assertEqual( response.status_code, 200 )
        native_response = response.native
        for thread in native_response:
            self.assertIsInstance( thread, Thread )
            self.assertEqual( thread.parameters[ 'board' ], 'w' )
            self.assertIsInstance( thread.parameters[ 'thread_number' ], int )
            self.assertIsInstance(
                thread.parameters[ 'last_modified' ], datetime.datetime )
