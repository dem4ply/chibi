from unittest import TestCase
import tempfile, shutil


class Test_with_files( TestCase ):
    amount_of_files = 3
    amount_of_dirs = 3

    def setUp(self):
        self.root_dir = tempfile.mkdtemp()
        self.empty_folder = tempfile.mkdtemp()
        self.files = [
            tempfile.mkstemp( dir=self.root_dir )[0]
            for i in range( self.amount_of_files ) ]
        self.dirs = [
            tempfile.mkdtemp( dir=self.root_dir )
            for i in range( self.amount_of_dirs ) ]

    def tearDown(self):
        shutil.rmtree( self.root_dir )
        shutil.rmtree( self.empty_folder )
