import './Chatbox.css';

function Chatbox(props) {
    return (
      <>
        <div className="conversation-container">
          {props.conversation.length === 0 && (
            <p id="title">Furnichanter AI</p>
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
                  <p className="query-text">{obj.text}</p>
                </div>
              )
            )
          }
        </div>
      </>
    )
  }
  
  export default Chatbox
  