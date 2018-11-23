import React from 'react';
import ReturnLine from './ReturnLine';

const ReturnLists = ({books, returnBook}) => {
    const allBooks = books.map((book, index) => (
        <ReturnLine key={index} book_id={book.book_id} book_name={book.book_name} author={book.author}
                    genre={book.genre} rent_date={book.rent_date} returnBook={returnBook}/>
    ));
    return (
        <div>
            <h1>Return A Book</h1>
            <table className="book-list">
                <thead>
                <tr>
                    <th>Book_Name</th>
                    <th>Author</th>
                    <th>Genre</th>
                    <th>Rent_Date</th>
                </tr>
                </thead>
                <tbody>{allBooks}</tbody>
            </table>
        </div>
    );
};
export default ReturnLists;