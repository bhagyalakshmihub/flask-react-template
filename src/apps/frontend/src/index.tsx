import React from 'react';
import ReactDOM from 'react-dom/client';
import Comments from './components/Comments';
import 'bootstrap/dist/css/bootstrap.min.css';

const container = document.getElementById('app');
const root = ReactDOM.createRoot(container!);
root.render(
  <React.StrictMode>
    <Comments />
  </React.StrictMode>,
);
