import random

from faker import Factory as Faker_factory

from chibi.file.snippets import ln, stat
from tests.snippet.files import Test_with_files


faker = Faker_factory.create()


class Test_ln( Test_with_files ):
    def test_when_create_a_simbolic_link_should_work( self ):
        file = random.choice( self.files )
        new_link = file.dir_name + 'asdf'
        self.assertFalse( new_link.exists )
        ln( file, new_link )
        self.assertTrue( new_link.exists )
        info = stat( new_link )
        self.assertTrue( info.is_link )
        self.assertEqual( info.link_target, file )
