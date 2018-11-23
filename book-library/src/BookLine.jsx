import React from 'react';

const BookLine = ({book_id, book_name, author, genre, available, rentBook}) => {
    return (
        <tr>
            <td className="book_name">{book_name}</td>
            <td className="author">{author}</td>
            <td className="genre">{genre}</td>
            <td className="available">{available.toString()}</td>
            <td>
                <button onClick={() => rentBook(book_id)} disabled={!available}>Rent</button>
            </td>
        </tr>
    );
};

export default BookLine;
