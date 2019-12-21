from unittest import TestCase
from chibi.metaphors import Book
from chibi.metaphors.book import End_book


class Test_book( TestCase ):
    def test_total_of_pages( self ):
        book = Book( total_elements=10, page_size=1 )
        self.assertEqual( book.total_pages, 10 )
        book = Book( total_elements=10, page_size=5 )
        self.assertEqual( book.total_pages, 2 )
        book = Book( total_elements=10, page_size=3 )
        self.assertEqual( book.total_pages, 4 )

    def test_next_should_increase_the_page( self ):
        book = Book( total_elements=10, page_size=3 )
        self.assertEqual( book.page, 1 )
        book.next()
        self.assertEqual( book.page, 2 )
        book.next()
        self.assertEqual( book.page, 3 )
        book.next()
        self.assertEqual( book.page, 4 )

    def test_with_next_should_raise_end_of_book( self ):
        book = Book( total_elements=10, page_size=3 )
        self.assertEqual( book.page, 1 )
        book.next()
        self.assertEqual( book.page, 2 )
        book.next()
        self.assertEqual( book.page, 3 )
        book.next()
        self.assertEqual( book.page, 4 )
        with self.assertRaises( End_book ):
            book.next()
        self.assertEqual( book.page, 4 )

    def test_prev_should_decrease_the_page( self ):
        book = Book( total_elements=10, page_size=3, page=4 )
        self.assertEqual( book.page, 4 )
        book.prev()
        self.assertEqual( book.page, 3 )
        book.prev()
        self.assertEqual( book.page, 2 )
        book.prev()
        self.assertEqual( book.page, 1 )

    def test_with_prev_should_raise_end_of_book( self ):
        book = Book( total_elements=10, page_size=3, page=4 )
        self.assertEqual( book.page, 4 )
        book.prev()
        self.assertEqual( book.page, 3 )
        book.prev()
        self.assertEqual( book.page, 2 )
        book.prev()
        self.assertEqual( book.page, 1 )
        with self.assertRaises( End_book ):
            book.prev()
        self.assertEqual( book.page, 1 )
