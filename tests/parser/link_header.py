import unittest

from chibi.atlas import Chibi_atlas
from chibi.parser import link_header


class Test_link_header( unittest.TestCase ):

    def test_single_link( self ):
        header = '<https://example.com/page/2>; rel="next"'

        result = link_header( header )

        self.assertIsInstance( result, Chibi_atlas )
        self.assertEqual(
            result["next"],
            "https://example.com/page/2",
        )

    def test_multiple_links( self ):
        header = (
            '<https://example.com/page/1>; rel="first", '
            '<https://example.com/page/2>; rel="next", '
            '<https://example.com/page/10>; rel="last"'
        )
        result = link_header( header )
        self.assertEqual(
            result,
            {
                "first": "https://example.com/page/1",
                "next": "https://example.com/page/2",
                "last": "https://example.com/page/10",
            },
        )

    def test_link_with_spaces( self ):
        header = '<https://example.com/page/2> ; rel="next"'
        result = link_header( header )
        self.assertEqual(
            result["next"],
            "https://example.com/page/2",
        )

    def test_invalid_link_without_rel( self ):
        header = '<https://example.com/page/2>'
        result = link_header( header )
        self.assertEqual( result, {})

    def test_invalid_link_without_angle_brackets( self ):
        header = 'https://example.com/page/2; rel="next"'
        result = link_header( header )
        self.assertEqual( result, {})

    def test_custom_link_delimiter( self ):
        header = (
            '<https://example.com/page/1>| rel="first" ; '
            '<https://example.com/page/2>| rel="next"'
        )
        result = link_header(
            header, link_delimiter=";", param_delimiter="|", )

        self.assertEqual( result[ "first" ], "https://example.com/page/1", )
        self.assertEqual( result[ "next" ], "https://example.com/page/2", )

    def test_empty_header( self ):
        result = link_header("")
        self.assertEqual( result, {})
