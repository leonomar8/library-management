# test_library.py

import pytest
from datetime import datetime, timedelta
from book import Book
from user import User
from library import Library

def test_borrow_available_book():
    '''
    The book gets marked as borrowed.
    The book is linked to the correct user.
    The due date is exactly 14 days from today.
    The book appears in the user’s borrowed list.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    library.add_book(book)
    library.add_user(alice)
    today = datetime.now().date()
    expected_due = today + timedelta(days=14)

    # Act
    library.borrow_book("1984", alice)  # Should work fine

    # Assert
    assert book.available == False
    assert book.borrowed_by.name == "Alice"
    assert book.due_date == expected_due
    assert book in alice.books_borrowed

def test_borrow_book_already_borrowed():
    '''
    2. A user cannot borrow a book that is already borrowed
        1.1 The system raises an appropriate error or exception when the book is already marked as borrowed.
        1.2 The user’s borrowed books list remains unchanged after the failed attempt.
        1.3 The book's borrowed_by field still points to the original borrower.
        1.4 The book's due_date remains unchanged after the second borrow attempt.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book)
    library.add_user(alice)
    library.add_user(bob)

    # Act
    library.borrow_book("1984", alice)  # Should succeed
    due_date_expected = datetime.now().date() + timedelta(days=14)

    # Assert (after Alice borrows)
    assert book.available == False
    assert book.borrowed_by.name == "Alice"
    assert book.due_date == due_date_expected
    assert book in alice.books_borrowed
    assert book not in bob.books_borrowed

    # Act & Assert (Bob tries to borrow and fails)
    with pytest.raises(ValueError, match=f"❌ Hi {bob.name} the book '{book.title}' is not available, it is already borrowed to {book.borrowed_by.name}."):
        library.borrow_book("1984", bob)

    # Re-Assert nothing changed
    assert book.borrowed_by.name == "Alice"
    assert book.due_date == due_date_expected
    assert book not in bob.books_borrowed

def test_book_assigned_to_user_with_right_due_date():

    '''
    3. A book is correctly assigned to the user with the correct due date
        2.1 The book's borrowed_by field matches the user who borrowed it.
        2.2 The book's due_date is 14 days from the date of borrowing.
        2.3 The book's available flag is set to False.
        2.4 The book appears in the user's borrowed_books list.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    library.add_book(book)
    library.add_user(alice)

    # Act
    library.borrow_book("1984", alice)  # Should succeed
    due_date_expected = datetime.now().date() + timedelta(days=14)

    # Assert (after Alice borrows)
    assert book.available == False
    assert book.borrowed_by.name == "Alice"
    assert book.due_date == due_date_expected
    assert book in alice.books_borrowed


def test_return_borrowed_book():
    '''
    4. A user can return a borrowed book
        3.1 The book's available flag is set to True after return.
        3.2 The book's borrowed_by and due_date fields are cleared or set to None.
        3.3 The book is removed from the user's books_borrowed list.
        3.4 The system allows the book to be borrowed again by the same or a different user.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book)
    library.add_user(alice)
    library.add_user(bob)

    # Act
    library.borrow_book("1984", alice)  # Should succeed
    library.return_book("1984", alice)  # Should succeed

    # Assert (after Alice return)
    assert book.available == True
    assert book.borrowed_by is None
    assert book.due_date is None
    assert book not in alice.books_borrowed

    # Act
    library.borrow_book("1984", alice)  # Should succeed

    # Assert (after Alice borrows)
    assert book.available == False
    assert book.borrowed_by.name == "Alice"
    assert book.due_date is not None
    assert book in alice.books_borrowed

    # Act
    library.return_book("1984", alice)  # Should succeed
    library.borrow_book("1984", bob)    # Should succeed

    # Assert (after Alice return and Bob borrows)
    assert book.available == False
    assert book.borrowed_by.name == "Bob"
    assert book.due_date is not None
    assert book in bob.books_borrowed


def test_return_book_makes_it_available_again():
    '''
    5. Returning a book makes it available again
        4.1 The book can be successfully borrowed again by another user after it’s returned.
        4.2 The new borrower is updated correctly in the book’s borrowed_by field.
        4.3 The new borrow triggers a fresh due date 14 days from the new borrow date.
        4.4 No error or restriction occurs when re-borrowing the returned book.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book)
    library.add_user(alice)
    library.add_user(bob)

    # Act
    library.borrow_book("1984", alice)  # Should succeed
    library.return_book("1984", alice)  # Should succeed
    library.borrow_book("1984", bob)    # Should succeed
    due_date_expected = datetime.now().date() + timedelta(days=14)

    # Assert (after Alice return and Bob borrows)
    assert book.available == False
    assert book.borrowed_by.name == "Bob"
    assert book.due_date == due_date_expected
    assert book in bob.books_borrowed


def test_fine_is_calculated_if_book_is_returned_late():
    '''
    6. A fine is correctly calculated if a book is returned late
        5.1 Returning a book past the due date triggers a fine calculation.
        5.2 The fine amount matches the expected value based on days overdue.
        5.3 The fine is zero if the book is returned on or before the due date.
        5.4 The calculated fine is associated with the correct user or return transaction.
    '''
    # Arrange
    library = Library()
    book = Book("1984", "George Orwell")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book)
    library.add_user(alice)
    library.add_user(bob)

    # Act
    library.borrow_book("1984", alice)  # Should succeed
    book.due_date = datetime.now().date() - timedelta(days=10)
    library.return_book("1984", alice)  # Should succeed

    # Assert (fine after Alice returns overdue)
    assert alice.total_fines > 0
    assert alice.total_fines == 10

    # Act
    library.borrow_book("1984", bob)  # Should succeed
    book.due_date = datetime.now().date() + timedelta(days=14)
    library.return_book("1984", bob)  # Should succeed

    # Assert (no fine if Bob returns on due_date)
    assert bob.total_fines == 0

    # Act
    library.borrow_book("1984", bob)  # Should succeed
    book.due_date = datetime.now().date() + timedelta(days=13)
    library.return_book("1984", bob)  # Should succeed

    # Assert (no fine if Bob returns before due_date)
    assert bob.total_fines == 0


def test_add_borrowed_book_to_user_list():        
    '''
    7. Borrowing a book adds it to the user’s list
        6.1 The book appears in the user’s borrowed_books list after borrowing.
        6.2 The list length increases by 1 after each successful borrow.
        6.3 The list contains only books that the user currently has borrowed.
        6.4 The list does not contain books returned by the user.
    '''
    # Arrange
    library = Library()
    book1 = Book("1984", "George Orwell")
    book2 = Book("To Kill a Mockingbird", "Harper Lee")
    book3 = Book("Brave New World", "Aldous Huxley")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_user(alice)
    library.add_user(bob)

    # Act
    library.borrow_book("1984", alice)  # Should succeed

    # Assert (after Alice borrows)
    assert book1.borrowed_by.name == "Alice"
    assert book1 in alice.books_borrowed
    assert len(alice.books_borrowed) == 1
    assert book2.borrowed_by is None
    assert book3.borrowed_by is None

    # Act
    library.borrow_book("To Kill a Mockingbird", alice)  # Should succeed

    # Assert (after Alice borrows)
    assert book2.borrowed_by.name == "Alice"
    assert book2 in alice.books_borrowed
    assert len(alice.books_borrowed) == 2
    assert book3 not in alice.books_borrowed

    # Act
    library.return_book("To Kill a Mockingbird", alice)  # Should succeed

    # Assert (after Alice returns)
    assert book2.borrowed_by is None
    assert book2 not in alice.books_borrowed
    assert len(alice.books_borrowed) == 1
    assert book3 not in alice.books_borrowed

def test_users_cannot_borrow_same_book_at_the_same_time():
    '''
    8. Multi-user scenario: Alice and Bob cannot borrow the same book at the same time
        7.1 If Alice borrows a book, Bob cannot borrow the same book until it is returned.
        7.2 Bob receives an appropriate error or exception if he attempts to borrow it.
        7.3 The book’s borrowed_by field only reflects Alice while the book is borrowed.
        7.4 Once Alice returns the book, Bob can borrow it and becomes the new borrowed_by.
    '''
    # Arrange
    library = Library()
    book1 = Book("1984", "George Orwell")
    book2 = Book("To Kill a Mockingbird", "Harper Lee")
    book3 = Book("Brave New World", "Aldous Huxley")
    alice = User("Alice")
    bob = User("Bob")
    library.add_book(book1)
    library.add_book(book2)
    library.add_book(book3)
    library.add_user(alice)
    library.add_user(bob)

    # Act & Assert (Bob tries to borrow and fails)
    library.borrow_book("1984", alice)  # Should succeed

    with pytest.raises(ValueError, match=f"❌ Hi {bob.name} the book '{book1.title}' is not available, it is already borrowed to {book1.borrowed_by.name}."):
        library.borrow_book("1984", bob)    
    
    # Assert (after Alice borrows)
    assert book1.borrowed_by.name == "Alice"
    assert book1 in alice.books_borrowed
    assert book1 not in bob.books_borrowed

    # Act & Assert (Bob tries to borrow and fails)
    library.return_book("1984", alice)  # Should succeed
    library.borrow_book("1984", bob) 

    # Assert (after Alice borrows)
    assert book1.borrowed_by == bob
    assert book1 in bob.books_borrowed
    assert book1 not in alice.books_borrowed