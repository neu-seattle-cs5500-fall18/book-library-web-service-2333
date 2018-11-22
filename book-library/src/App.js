import React, {Component} from 'react';
import './App.css';
import Login from './Login';
import Register from './Register'
import Loggedin from './Loggedin';
import BookLists from './BookLists';
import ReturnLists from './ReturnLists';
import {getUsers, postUsers, getBooks, rentABook, getRentBooks, returnABook} from './service';

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLogin: false,
            currentUser: '',
            user_id: null,
            loginUsername: '',
            loginPassword: '',
            registerUsername: '',
            registerPassword: '',
            books: [],
            rentRecords: []
        };
        this.onLoginUsername = this.onLoginUsername.bind(this);
        this.onLoginPassword = this.onLoginPassword.bind(this);
        this.onRegisterUsername = this.onRegisterUsername.bind(this);
        this.onRegisterPassword = this.onRegisterPassword.bind(this);
        this.onCheckForLogin = this.onCheckForLogin.bind(this);
        this.onCheckForRegister = this.onCheckForRegister.bind(this);
        this.onLogin = this.onLogin.bind(this);
        this.onRegister = this.onRegister.bind(this);
        this.onLogout = this.onLogout.bind(this);
        this.rentBook = this.rentBook.bind(this);
        this.returnBook = this.returnBook.bind(this);
        this.getAllBooks = this.getAllBooks.bind(this);
        this.getAllRentBooks = this.getAllRentBooks.bind(this);
    }

    onLoginUsername(e) {
        const text = e.target.value;
        this.setState({
            loginUsername: text
        });
    }

    onLoginPassword(e) {
        const text = e.target.value;
        this.setState({
            loginPassword: text
        });
    }

    onRegisterUsername(e) {
        const text = e.target.value;
        this.setState({
            registerUsername: text
        });
    }

    onRegisterPassword(e) {
        const text = e.target.value;
        this.setState({
            registerPassword: text
        });
    }

    onCheckForLogin(e) {
        if (e.key === "Enter") {
            this.onLogin();
        }
    }

    onCheckForRegister(e) {
        if (e.key === "Enter") {
            this.onLogin();
        }
    }

    onLogin() {
        if (this.state.loginUsername.length === 0 || this.state.loginPassword.length === 0) {
            alert("Empty username or password is invalid!");
        } else {
            getUsers()
                .then((users) => {
                    let user = users.filter(user => JSON.parse(user).username === this.state.loginUsername);
                    if (user.length === 0) {
                        alert("No such username!");
                        return Promise.reject('Wrong username!')
                    }
                    user = JSON.parse(user);
                    if (user === null || user.password !== this.state.loginPassword) {
                        alert("Wrong password!");
                        return Promise.reject('Wrong password!')
                    }
                    this.setState({
                        isLogin: true,
                        currentUser: this.state.loginUsername,
                        user_id: user.user_id
                    });
                })
                .then(() => {
                    this.getAllBooks();
                    this.getAllRentBooks();
                })
                .catch(err => console.log(err.message));
        }
    }

    onRegister() {
        if (this.state.registerUsername.length === 0 || this.state.registerPassword.length === 0) {
            alert("Empty username or password is invalid!");
        } else {
            getUsers()
                .then((users) => {
                    let user = users.filter(user => JSON.parse(user).username === this.state.registerUsername);
                    if (user.length !== 0) {
                        alert("Username already exists!");
                        return Promise.reject('Username already exists!')
                    }
                })
                .then(() => {
                    postUsers({username: this.state.registerUsername, password: this.state.registerPassword})
                })
                .then((user_id) => {
                    this.setState({
                        currentUser: this.state.registerUsername,
                        isLogin: true,
                        user_id: user_id
                    });
                })
                .then(() => {
                    this.getAllBooks();
                    this.getAllRentBooks();
                })
                .catch(err => console.log(err.message));
        }
    }

    onLogout() {
        this.setState({
            isLogin: false,
            currentUser: '',
            loginUsername: '',
            loginPassword: '',
            registerUsername: '',
            registerPassword: ''
        })
    }

    getAllBooks() {
        getBooks()
            .then((books) => {
                books = books.map((book) => (JSON.parse(book)));
                this.setState({
                    books: books
                })
            })
    }

    rentBook(book_id) {
        rentABook(this.state.user_id, book_id, Date.now())
            .then(this.getAllBooks)
            .then(this.getAllRentBooks);
    }

    getAllRentBooks() {
        getRentBooks(this.state.user_id)
            .then((books) => {
                books = books.map((book) => (JSON.parse(book)));
                this.setState({
                    rentRecords: books
                })
            })
    }

    returnBook(book_id) {
        returnABook(this.state.user_id, book_id, Date.now())
            .then(this.getAllBooks)
            .then(this.getAllRentBooks);
    }

    render() {

        const showLogin = !this.state.isLogin;

        return (
            <div className="App">
                {showLogin &&
                <div>
                    <Login
                        onLoginUsername={this.onLoginUsername}
                        onLoginPassword={this.onLoginPassword}
                        onCheckForLogin={this.onCheckForLogin}
                        onLogin={this.onLogin}
                        loginUsername={this.state.loginUsername}
                        loginPassword={this.state.loginPassword}
                    />
                    <Register
                        onRegisterUsername={this.onRegisterUsername}
                        onRegisterPassword={this.onRegisterPassword}
                        onCheckForRegister={this.onCheckForRegister}
                        onRegister={this.onRegister}
                        registerUsername={this.state.registerUsername}
                        registerPassword={this.state.registerPassword}
                    />
                </div>}
                {!showLogin &&
                <div>
                    <Loggedin
                        onLogout={this.onLogout}
                        currentUser={this.state.currentUser}
                    />
                    <BookLists
                        books={this.state.books}
                        rentBook={this.rentBook}
                    />
                    <ReturnLists
                        books={this.state.rentRecords}
                        returnBook={this.returnBook}/>
                </div>}
            </div>
        );
    }
}

export default App;
