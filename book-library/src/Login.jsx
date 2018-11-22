import React from 'react';

const Login = ({
                   onLoginUsername, onLoginPassword, onCheckForLogin,
                   loginUsername, onLogin, loginPassword
               }) => {

    return (
        <div className="login-area">
            <p>Login</p>
            <label>Username:</label>
            <input onChange={onLoginUsername} onKeyUp={onCheckForLogin} value={loginUsername} className="login"/>
            <label>Password:</label>
            <input onChange={onLoginPassword} onKeyUp={onCheckForLogin} value={loginPassword} className="login"/>
            <button onClick={onLogin} className="send-login" disabled={!loginUsername || !loginPassword}>login</button>
        </div>
    );
};
export default Login;