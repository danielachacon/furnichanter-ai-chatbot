import './Chatbox.css';
import ReactMarkdown from 'react-markdown';
import { useTypewriter, Cursor } from 'react-simple-typewriter';
import React, { useState, useEffect } from 'react';
import Loader  from './Loader'
function Chatbox(props) {
  const [text] = useTypewriter({
    words: ['Furnichanter AI', 'Your AI Furniture Assistant'],
    loop:{},
  });
  return (
      <>
        <div className="conversation-container">
          {props.conversation.length === 0 &&  (
            <div className='title-container'>
              <span id="title">
                {text}
              </span>
            </div>
          )}
          {
            props.conversation.map((obj,index) => 
              obj.type === "query" ? (
                <div key={index} className="conversation-query query-container" >
                  <p className="query-text">{obj.text}</p>
                </div>
              ) : (
                <div key={index} className="conversation-response query-container">
                  <img className="furnichanter-logo" src="/furnichanter.jpg" alt="Furnichanter" />
                  <ReactMarkdown className="query-text">{obj.text}</ReactMarkdown>
                </div>
              )
            )
          }
        </div>
      </>
    )
  }
  
  export default Chatbox
  