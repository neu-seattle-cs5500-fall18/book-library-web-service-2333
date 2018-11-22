import React from 'react';

const BookList = ({book_name, author, publish_date}) => {
    return (<div>
    <span className="book_name">{book_name}</span>,
    <span className="author">{author}</span>,
    <span className="publish_date">{publish_date}</span>
    </div>);
};

export default BookList;
