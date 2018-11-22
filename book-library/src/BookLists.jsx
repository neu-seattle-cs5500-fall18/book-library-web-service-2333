import React from 'react';
import BookList from './BookList';

const BookLists = ({books, rentBook}) => {
    const allBooks = books.map((book) => (
        <li key={book.book_id}>
            <BookList book_name={book.book_name} author={book.author} publish_date={book.publish_date}/>
            <button onClick={rentBook(book.book_id)}>Rent</button>
        </li>
    ));
    return (
        <div className="book-list">
            <ul className="book-line">
                {allBooks}
            </ul>
        </div>
    );
};
export default BookLists;
