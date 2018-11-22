import React from 'react';

const Register = ({
                      onRegisterUsername, onRegisterPassword, onCheckForRegister,
                      onRegister, registerUsername, registerPassword
                  }) => {

    return (
        <div className="register-area">
            <p>Register</p>
            <label>Username:</label>
            <input onChange={onRegisterUsername} onKeyUp={onCheckForRegister} value={registerUsername}
                   className="register"/>
            <label>Password:</label>
            <input onChange={onRegisterPassword} onKeyUp={onCheckForRegister} value={registerPassword}
                   className="login"/>
            <button onClick={onRegister} className="send-register"
                    disabled={!registerUsername || !registerPassword}>register
            </button>
        </div>
    );
};
export default Register;