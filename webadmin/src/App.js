import logo from './logo.svg';
import './App.css';
import { useEffect, useState } from 'react';
import { helloWorld } from './service/WebServerApi';

function App() {
  const [text, setText] = useState('');
  useEffect(() => {
    helloWorld()
      .then((res) => {
        console.log('Response from webserver: ', res.data);
        setText(res?.data?.data);
      })
      .catch((err) => {
        console.log('Error from webserver: ', err);
        setText('Has an error when call to webserver');
      });
  }, []);
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>{text}</p>
      </header>
    </div>
  );
}

export default App;
