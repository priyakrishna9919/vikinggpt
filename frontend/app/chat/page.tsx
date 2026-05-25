// =============================================
// VikingGPT Chat Page
// BearcatGPT-style UI with CSU green branding
// Streams responses from the FastAPI backend
// =============================================

"use client";

import { useState, useRef, useEffect } from "react";
import Sidebar from "@/components/Sidebar";
import ChatMessage from "@/components/ChatMessage";
import AgentCards from "@/components/AgentCards";

export type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: string[];
};

export default function ChatPage() {
  // Which view is active: "home" (agent cards) or "chat"
  const [view, setView] = useState<"home" | "chat">("home");
  const [activeAgent, setActiveAgent] = useState("Viking Chat");
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to the latest message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  // Open an agent and show the welcome message
  function openAgent(agentName: string) {
    setActiveAgent(agentName);
    setView("chat");
    setMessages([{
      role: "assistant",
      content: `Hi! I'm VikingGPT, your Cleveland State University assistant 🏛️\n\nI search csuohio.edu to give you accurate, real-time answers about:\n• Admissions & deadlines\n• Tuition & financial aid\n• Housing & rec center hours\n• Programs, calendar, staff & more\n\nWhat would you like to know about CSU?`,
    }]);
  }

  // Send user message and stream back the response
  async function sendMessage() {
    const text = input.trim();
    if (!text || isLoading) return;

    const userMsg: Message = { role: "user", content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
      const encoded = encodeURIComponent(text);

      // Connect to the SSE streaming endpoint
      const response = await fetch(`${apiUrl}/api/chat/stream?question=${encoded}`);
      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      let assistantText = "";
      let sources: string[] = [];

      // Add a placeholder message for the streaming response
      setMessages(prev => [...prev, { role: "assistant", content: "" }]);

      // Read the stream token by token
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const chunk = decoder.decode(value);
        const lines = chunk.split("\n").filter(l => l.startsWith("data: "));

        for (const line of lines) {
          const data = JSON.parse(line.slice(6));

          if (data.token) {
            // Append each token to the message in real time
            assistantText += data.token;
            setMessages(prev => {
              const updated = [...prev];
              updated[updated.length - 1] = { role: "assistant", content: assistantText };
              return updated;
            });
          }

          if (data.done) {
            sources = data.sources || [];
            // Attach sources to the final message
            setMessages(prev => {
              const updated = [...prev];
              updated[updated.length - 1] = { role: "assistant", content: assistantText, sources };
              return updated;
            });
          }
        }
      }
    } catch (err) {
      console.error("Chat error:", err);
      setMessages(prev => [...prev, {
        role: "assistant",
        content: "Sorry, I had trouble reaching CSU's database. Please try again or call (216) 687-2000.",
      }]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleKeyDown(e: React.KeyboardEvent) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  }

  return (
    <div className="flex h-screen bg-gray-100 overflow-hidden">

      {/* CSU green sidebar */}
      <Sidebar
        onNewChat={() => setView("home")}
        onSelectAgent={openAgent}
        activeAgent={view === "chat" ? activeAgent : null}
      />

      {/* Main panel */}
      <main className="flex-1 flex flex-col bg-white overflow-hidden">

        {/* HOME VIEW: agent cards grid */}
        {view === "home" && (
          <AgentCards onSelectAgent={openAgent} />
        )}

        {/* CHAT VIEW: conversation thread */}
        {view === "chat" && (
          <>
            {/* Chat header */}
            <div className="flex items-center justify-between px-6 py-3 border-b border-gray-200">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full flex items-center justify-center text-white text-xs font-semibold"
                  style={{ background: "var(--csu-green)" }}>V</div>
                <span className="font-semibold text-gray-800">{activeAgent}</span>
                <span className="text-xs bg-green-100 text-green-700 px-2 py-0.5 rounded-full font-medium">✓ Official</span>
              </div>
              <button
                onClick={() => setView("home")}
                className="text-sm text-gray-500 border border-gray-200 rounded-lg px-3 py-1.5 hover:border-green-700 hover:text-green-700 transition-colors"
              >
                ← Back to Agents
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto px-6 py-5 space-y-4">
              {messages.map((msg, i) => (
                <ChatMessage key={i} message={msg} />
              ))}

              {/* Typing indicator */}
              {isLoading && (
                <div className="flex items-center gap-3">
                  <div className="w-7 h-7 rounded-full flex items-center justify-center text-white text-xs font-bold"
                    style={{ background: "var(--csu-green)" }}>V</div>
                  <div className="bg-gray-100 border border-gray-200 rounded-2xl rounded-bl-sm px-4 py-3 flex items-center gap-2">
                    <div className="flex gap-1">
                      {[0, 1, 2].map(i => (
                        <div key={i} className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce"
                          style={{ animationDelay: `${i * 0.15}s` }} />
                      ))}
                    </div>
                    <span className="text-xs text-gray-400">Searching csuohio.edu...</span>
                  </div>
                </div>
              )}
              <div ref={messagesEndRef} />
            </div>

            {/* Input */}
            <div className="px-6 py-4 border-t border-gray-200">
              <div className="flex items-end gap-3 bg-gray-50 border border-gray-200 rounded-xl px-4 py-3 focus-within:border-green-700 focus-within:ring-2 focus-within:ring-green-100 transition-all">
                <textarea
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={handleKeyDown}
                  placeholder="Message VikingGPT..."
                  rows={1}
                  className="flex-1 bg-transparent resize-none outline-none text-sm text-gray-800 placeholder-gray-400"
                  style={{ maxHeight: "120px" }}
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !input.trim()}
                  className="w-9 h-9 rounded-lg flex items-center justify-center text-white disabled:opacity-40 transition-opacity"
                  style={{ background: "var(--csu-green)" }}
                >
                  <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
                    <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z"/>
                  </svg>
                </button>
              </div>
              <p className="text-xs text-gray-400 mt-2 text-center">
                Answers searched live from csuohio.edu · Enter to send · Shift+Enter for new line
              </p>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
