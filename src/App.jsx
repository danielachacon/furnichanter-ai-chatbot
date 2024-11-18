import { useState } from 'react'
import './App.css'
import Input from './components/input'
import Chatbox from './components/chatbox'

function App() {
  const [loading, setLoading] = useState(false);
  const [prompt, setPrompt] = useState("");
  const [conversation, setConversation] = useState([]);
  
  return (
    <>
      <Chatbox id="chat"
        conversation={conversation}
        loading={loading}
      />
      <Input id="textInput"
        prompt={prompt}
        loading={loading}
        conversation={conversation}
        setPrompt={setPrompt}
        setLoading={setLoading}
        setConversation={setConversation}/>
    </>
  )
}

export default App
