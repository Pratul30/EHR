import { render } from '@testing-library/react'
import React,{Component} from 'react'

class Message extends Component{
    constructor(){
        super()
        this.state={
            count:0
        }
    this.changeMessage=this.changeMessage.bind(this)
    }

changeMessage(){
    this.setState(
        {
            count:this.state.count+1
        }
    )
}


render(){
    return(
        <div>
            <div>{this.state.count}</div>
            <button onClick={this.changeMessage}>Click</button>
        </div>
    )
}
}

export default Message;