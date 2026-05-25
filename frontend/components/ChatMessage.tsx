// =============================================
// ChatMessage Component
// Renders a single user or assistant message
// Shows source URLs under assistant replies
// =============================================

"use client";
import type { Message } from "@/app/chat/page";

type Props = { message: Message };

export default function ChatMessage({ message }: Props) {
  const isBot = message.role === "assistant";

  return (
    <div className={`flex gap-3 ${isBot ? "" : "flex-row-reverse"}`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold flex-shrink-0 mt-0.5 ${
        isBot ? "text-white" : "text-green-800"
      }`} style={{ background: isBot ? "#0d4f2e" : "#6abf69" }}>
        {isBot ? "V" : "KP"}
      </div>

      <div className="flex flex-col gap-1 max-w-2xl min-w-0">
        {/* Message bubble */}
        <div className={`px-4 py-3 rounded-2xl text-sm leading-relaxed whitespace-pre-line ${
          isBot
            ? "bg-gray-100 border border-gray-200 rounded-bl-sm text-gray-800"
            : "text-white rounded-br-sm"
        }`} style={isBot ? {} : { background: "#0d4f2e" }}>
          {message.content}
        </div>

        {/* Source URLs shown under bot replies */}
        {isBot && message.sources && message.sources.length > 0 && (
          <div className="flex flex-wrap gap-1 px-1">
            {message.sources.map((url, i) => (
              <a key={i} href={url} target="_blank" rel="noopener noreferrer"
                className="text-xs px-2 py-0.5 rounded-full border flex items-center gap-1 transition-colors"
                style={{ color: "#0d4f2e", borderColor: "#0d4f2e22", background: "#0d4f2e0a" }}
                onMouseOver={e => (e.currentTarget.style.background = "#0d4f2e18")}
                onMouseOut={e => (e.currentTarget.style.background = "#0d4f2e0a")}
              >
                🔍 {new URL(url).hostname}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
