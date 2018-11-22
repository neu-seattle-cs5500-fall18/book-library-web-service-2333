import React from 'react';
import ReturnLine from './ReturnLine';

const ReturnLists = ({books, returnBook}) => {
    const allBooks = books.map((book, index) => (
        <ReturnLine key={index} book_id={book.book_id} book_name={book.book_name} author={book.author}
                    publish_date={book.publish_date} available={book.available} status={book.status}
                    rent_date={book.rent_date}
                    return_date={book.return_date}
                    returnBook={returnBook}/>
    ));
    return (
        <div>
            <h1>Return A Book</h1>
            <table className="book-list">
                <thead>
                <tr>
                    <th>Book_Name</th>
                    <th>Author</th>
                    <th>Publish_Date</th>
                    <th>Available</th>
                    <th>Status</th>
                    <th>Rent_Date</th>
                    <th>Return_Date</th>
                </tr>
                </thead>
                <tbody>{allBooks}</tbody>
            </table>
        </div>
    );
};
export default ReturnLists;