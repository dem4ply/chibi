from unittest import TestCase

from chibi.config import Configuration
from chibi.config.exception import Chibi_config_not_set


class Test_configuration_required( TestCase ):
    def setUp( self ):
        self.configuration = Configuration()

    def test_when_node_is_empty_should_raise_chibi_config_not_set( self ):
        with self.assertRaises( Chibi_config_not_set ):
            self.configuration.api.required()

    def test_when_node_is_empty_should_have_the_correct_option_name( self ):
        with self.assertRaises( Chibi_config_not_set ) as ctx:
            self.configuration.api.required()
        self.assertEqual( ctx.exception.option_name, 'api' )

    def test_when_node_has_values_should_not_raise( self ):
        self.configuration.api.host = 'localhost'
        result = self.configuration.api.required()
        self.assertIs( result, self.configuration.api )


class Test_configuration_require( TestCase ):
    def setUp( self ):
        self.configuration = Configuration()

    def test_when_value_is_set_should_return_the_value( self ):
        self.configuration.api.host = 'localhost'
        result = self.configuration.api.required( 'host' )
        self.assertEqual( result, 'localhost' )

    def test_when_value_is_not_set_should_raise_chibi_config_not_set( self ):
        with self.assertRaises( Chibi_config_not_set ):
            self.configuration.api.required( 'host' )

    def test_when_value_is_not_set_should_have_the_correct_option_name( self ):
        with self.assertRaises( Chibi_config_not_set ) as ctx:
            self.configuration.api.required( 'host' )
        self.assertEqual(
            ctx.exception.option_name, 'api.host' )

    def test_when_value_is_empty_string_should_raise( self ):
        self.configuration.api.host = ''
        with self.assertRaises( Chibi_config_not_set ):
            self.configuration.api.required( 'host' )

    def test_when_value_is_zero_should_raise( self ):
        self.configuration.api.port = 0
        with self.assertRaises( Chibi_config_not_set ):
            self.configuration.api.required( 'port' )

    def test_when_value_is_a_nonzero_int_should_return_it( self ):
        self.configuration.api.port = 5432
        result = self.configuration.api.required( 'port' )
        self.assertEqual( result, 5432 )

    def test_should_not_change_the_type_of_the_returned_value( self ):
        self.configuration.api.tags = [ 'a', 'b' ]
        result = self.configuration.api.required( 'tags' )
        self.assertIsInstance( result, list )
        self.assertEqual( result, [ 'a', 'b' ] )


class Test_configuration_require_from_root( TestCase ):
    def setUp( self ):
        self.configuration = Configuration()

    def test_when_path_has_multiple_levels_and_is_set_should_return_value(
            self ):
        connection = self.configuration.api.connection
        connection.host = 'localhost'
        result = self.configuration.required( 'api.connection.host' )
        self.assertEqual( result, 'localhost' )

    def test_when_path_has_multiple_levels_and_is_not_set_should_raise( self ):
        with self.assertRaises( Chibi_config_not_set ) as ctx:
            self.configuration.required( 'api.connection.host' )
        self.assertEqual(
            ctx.exception.option_name,
            'api.connection.host' )


class Test_chibi_config_not_set_exception( TestCase ):
    def test_should_build_the_correct_message( self ):
        exception = Chibi_config_not_set( 'api.host' )
        self.assertEqual(
            str( exception ),
            'no esta configurado api.host' )

    def test_should_store_the_option_name( self ):
        exception = Chibi_config_not_set( 'api.host' )
        self.assertEqual( exception.option_name, 'api.host' )
