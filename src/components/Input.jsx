import React, { useState, useEffect } from 'react'; // Added useEffect
import './Input.css';
import { FaArrowUp } from "react-icons/fa";

function Input(props) {

    useEffect(() => {
        console.log(props.conversation)
    }, [props.conversation]);

    const handleQuerySubmit = (event) => {
        event.preventDefault();
        props.setLoading(true);
        props.setConversation((prevData) => [
            ...prevData,
            {
                type: "query",
                text: props.prompt,
            }
        ]);
        const temp = props.prompt;
        props.setPrompt("");
        //response from server
        getResponseFromServer(temp);
    };

    const getResponseFromServer = async(temp) => {
        try {
            const response = await fetch("http://localhost:5500", {
                method:"POST",
                credentials: "include",
                headers: {
                    "Content-Type": "application/json"
                },
                body:JSON.stringify({prompt:temp}),
            })
            const responseData = await response.json()
            props.setConversation((prevData) => [
                ...prevData,
                {
                    type: "response",
                    text: responseData.response,
                },
            ]);
            props.setLoading(false);
        } catch (error) {
            props.setConversation((prevData) => [
                ...prevData,
                {
                    type:'response',
                    text:"Something went wrong!"
                }
            ]);
            props.setLoading(false);
        }
    };

    return (
      <>
        <form onSubmit={handleQuerySubmit}>
            <input id="input-text"
                name="input-text"
                type="text"
                placeholder="Message Furnichanter"
                value={props.prompt}
                onChange={(e) => props.setPrompt(e.target.value)}
                autoComplete="off">
            </input>
            <button id="upload" disabled={!props.prompt || props.loading}><FaArrowUp style={{ color: 'black' }} /></button>
        </form>
      </>
    )
  }
  
  export default Input
  