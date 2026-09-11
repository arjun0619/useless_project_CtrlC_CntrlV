import { useState } from "react";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const [sessionId] = useState(() => crypto.randomUUID());

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!input.trim() || loading) {
      return;
    }

    const userMessage = input.trim();

    // Add user's message to the screen
    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          session_id: sessionId,
          message: userMessage,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessages((prev) => [
          ...prev,
          {
            role: "ai",
            text: data.reply,
          },
        ]);
      } else {
        setMessages((prev) => [
          ...prev,
          {
            role: "ai",
            text: "Something went wrong. Try again.",
          },
        ]);
      }
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "ai",
          text: "I can't connect to the server right now.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <div className="app">

      <header className="header">
        <h1>AI Therapist</h1>
      </header>

      <main className="chat-area">

        <div className="messages">

          {messages.length === 0 && (
            <div className="welcome">
              <h2>Hey 👋</h2>
              <p>
                What's going on?
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={`message ${message.role}`}
            >
              {message.text}
            </div>
          ))}

          {loading && (
            <div className="message ai">
              Thinking...
            </div>
          )}

        </div>

        <form
          className="input-area"
          onSubmit={sendMessage}
        >

          <input
            type="text"
            placeholder="Tell me what's on your mind..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />

          <button type="submit">
            Send
          </button>

        </form>

      </main>

    </div>
  );
}

export default App;
