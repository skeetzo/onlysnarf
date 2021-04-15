import React from 'react';
import ReactDOM from 'react-dom';
import Example from './components/Example.jsx';

// Main Entry point function
function App() {
	return <Example/>;
}

// Rendering the entire react application
ReactDOM.render(<App/>, document.getElementById('root'));