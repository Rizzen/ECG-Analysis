import React from 'react';
import logo from './logo.svg';
import lg from './tensorflow-icon.svg';
import './App.css';

import SimpleReactFileUpload from "./Uploader";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={lg} className="App-logo" alt="logo" />
        <p>
          Upload file to get predictions
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
        </a>
          <SimpleReactFileUpload/>
      </header>
    </div>
  );
}

export default App;
