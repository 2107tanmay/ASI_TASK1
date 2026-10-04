import React, { useState } from "react";

export default function Chatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([{ sender: "bot", text: "Ask me a question about any figure. I only answer using verified evidence from the ledger." }]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userText = input.trim();
    setMessages((prev) => [...prev, { sender: "user", text: userText }]);
    setInput("");
    setIsLoading(true);

    try {
      const response = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: userText })
      });
      
      if (!response.ok) {
        throw new Error("Network error");
      }
      
      const data = await response.json();
      setMessages((prev) => [...prev, { sender: "bot", text: data.response }]);
    } catch (err) {
      setMessages((prev) => [...prev, { sender: "bot", text: "Sorry, the RAG backend is currently unavailable." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {isOpen ? (
        <div className="bg-white rounded-lg shadow-xl w-96 flex flex-col border border-slate-200" style={{ height: "450px" }}>
          <div className="bg-slate-800 text-white p-3 rounded-t-lg flex justify-between items-center">
            <span className="font-semibold text-sm">Evidence RAG Assistant</span>
            <button onClick={() => setIsOpen(false)} className="text-slate-300 hover:text-white">✕</button>
          </div>
          
          <div className="flex-1 p-4 overflow-y-auto flex flex-col gap-3 bg-slate-50">
            {messages.map((msg, idx) => (
              <div key={idx} className={`max-w-[85%] p-3 rounded text-sm whitespace-pre-wrap leading-relaxed ${msg.sender === "user" ? "bg-blue-100 text-blue-900 self-end rounded-br-none shadow-sm" : "bg-white border border-slate-200 text-slate-700 self-start rounded-bl-none shadow-sm"}`}>
                {msg.text}
              </div>
            ))}
            {isLoading && (
              <div className="bg-white border border-slate-200 text-slate-400 self-start rounded-bl-none shadow-sm p-3 rounded text-sm italic">
                Searching ledger...
              </div>
            )}
          </div>

          <form onSubmit={handleSend} className="border-t border-slate-200 p-3 bg-white rounded-b-lg flex gap-2">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about Option C, Capex, ARR..." 
              className="flex-1 px-3 py-2 text-sm border border-slate-300 rounded focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading} className={`bg-slate-800 text-white px-4 py-2 rounded text-sm font-semibold transition ${isLoading ? 'opacity-50' : 'hover:bg-slate-700'}`}>Send</button>
          </form>
        </div>
      ) : (
        <button 
          onClick={() => setIsOpen(true)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-full shadow-lg font-bold flex items-center gap-2 transition-transform transform hover:scale-105"
        >
          <span>Ask Evidence (RAG)</span>
        </button>
      )}
    </div>
  );
}
