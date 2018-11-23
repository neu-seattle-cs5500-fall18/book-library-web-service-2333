import React from 'react';
import BookLine from './BookLine';

const BookLists = ({books, rentBook}) => {
    const allBooks = books.map((book, index) => (
        <BookLine key={index} book_id={book.book_id} book_name={book.book_name} author={book.author}
                  genre={book.genre}
                  available={book.available} rentBook={rentBook}/>
    ));
    return (
        <div>
            <h1>All Books</h1>
            <table className="book-list">
                <thead>
                <tr>
                    <th>Book_Name</th>
                    <th>Author</th>
                    <th>Genre</th>
                    <th>Available</th>
                </tr>
                </thead>
                <tbody>{allBooks}</tbody>
            </table>
        </div>
    );
};
export default BookLists;
