import React from 'react';

const ReturnLine = ({
                        book_id, book_name, author, genre,
                        rent_date, return_date, returnBook
                    }) => {
    return (
        <tr>
            <td className="book_name">{book_name}</td>
            <td className="author">{author}</td>
            <td className="genre">{genre}</td>
            <td className="rent_date">{rent_date}</td>
            <td>
                <button onClick={() => returnBook(book_id)}>Return</button>
            </td>
        </tr>
    );
};

export default ReturnLine;
