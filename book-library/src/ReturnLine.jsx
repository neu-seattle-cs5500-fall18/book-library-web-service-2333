import React from 'react';

const ReturnLine = ({
                        book_id, book_name, author, publish_date,
                        available, status, rent_date, return_date, returnBook
                    }) => {
    return (
        <tr>
            <td className="book_name">{book_name}</td>
            <td className="author">{author}</td>
            <td className="publish_date">{publish_date}</td>
            <td className="available">{available.toString()}</td>
            <td className="status">{status}</td>
            <td className="rent_day">{rent_date}</td>
            <td className="return_day">{return_date}</td>
            <td>
                <button onClick={() => returnBook(book_id)} disabled={available || status === 'RETURN'}>Return</button>
            </td>
        </tr>
    );
};

export default ReturnLine;
