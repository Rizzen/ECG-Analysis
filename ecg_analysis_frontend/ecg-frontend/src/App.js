import React from 'react';
import lg from './ecg.svg';
import './App.css';

import SimpleReactFileUpload from "./Uploader";

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={lg} className="App-logo" alt="logo" />
        <h2>ECG Analyser</h2>
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
