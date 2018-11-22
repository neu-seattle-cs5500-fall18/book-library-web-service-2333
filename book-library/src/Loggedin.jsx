import React from 'react';

const Loggedin = ({onLogout, currentUser}) => {

  return (
      <div className="logged-in-area">
          <p> user: {currentUser} </p>
          <button onClick={onLogout} className="logout">logout</button>
      </div>
  );
};

export default Loggedin;