import { useEffect, useRef, useState } from "react";
import "./App.css";
import LandingPage from "./landingpage";

function App() {
  const [started, setStarted] = useState(false);

  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const [sessionId] = useState(() => crypto.randomUUID());

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages, loading]);

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
      const response = await fetch(
        "https://dr-brutally-honest.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            session_id: sessionId,
            message: userMessage,
          }),
        }
      );

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

  // Show landing page before starting the therapist
  if (!started) {
    return (
      <LandingPage
        onStart={() => setStarted(true)}
      />
    );
  }

  // Show therapist after clicking START
  return (
    <div className="app">

      <header className="header">
        <h1>Dr Brutally Honest</h1>
      </header>

      <main className="chat-area">

        <div className="messages">

          {messages.length === 0 && (
            <div className="welcome">
              <h2>Welcome</h2>
              <p>
                What problem are we pretending we can solve today?
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
              .....
            </div>
          )}

          <div ref={messagesEndRef} />

        </div>

        <form
          className="input-area"
          onSubmit={sendMessage}
        >

          <input
            type="text"
            placeholder=""
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