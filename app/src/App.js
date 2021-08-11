import React,{Component} from 'react';
import './App.css';
import Message from './greet.js'

class App extends Component{
  render(){
  return(
    <div className='App'>
      <Message name='pratul'/>
    </div>
    );
  }
}

export default App;