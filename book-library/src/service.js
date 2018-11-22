export const getUsers = () => {
    return fetch('/users')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error(response.statusText);
        });
};

export const postUsers = ({username, password}) => {
    return fetch('/users', {
        method: "POST",
        body: JSON.stringify({username, password}),
        headers: new Headers({'content-type': 'application/json'}),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.statusText);
            }
        });
};

export const getBooks = () => {
    return fetch('/books')
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error(response.statusText);
        });
};

export const rentABook = (user_id, book_id, rent_date) => {
    let url = '/rent_return' + user_id + book_id;
    return fetch(url, {
        method: "POST",
        body: JSON.stringify({rent_date}),
        headers: new Headers({'content-type': 'application/json'}),
    })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error(response.statusText);
            }
        });
};