from unittest import TestCase
from chibi import madness


class Test_generate_token_b64( TestCase ):
    def test_should_no_return_a_empty_string( self ):
        self.assertTrue( madness.string.generate_token_b64 )
