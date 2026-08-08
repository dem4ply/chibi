import datetime
from unittest import TestCase

from chibi.snippet.datetime import today


class Test_today( TestCase ):
    def test_should_work( self ):
        result = today()
        self.assertIsInstance( result, datetime.datetime )

    def test_is_utc_by_default( self ):
        result = today()
        self.assertEqual( result.tzinfo, datetime.timezone.utc )
