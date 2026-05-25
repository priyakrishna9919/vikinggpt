// =============================================
// Sidebar Component
// CSU green left panel — matches BearcatGPT style
// =============================================

"use client";

type SidebarProps = {
  onNewChat: () => void;
  onSelectAgent: (name: string) => void;
  activeAgent: string | null;
};

// Recent chat history items shown in the sidebar
const RECENT_CHATS = [
  "Rec Center Hours",
  "Process For Applying To A...",
  "Tuition & Financial Aid",
  "Housing & Dorms",
];

export default function Sidebar({ onNewChat, onSelectAgent, activeAgent }: SidebarProps) {
  return (
    <aside className="w-64 min-w-64 flex flex-col text-white" style={{ background: "#0d4f2e" }}>

      {/* Brand header */}
      <div className="px-4 pt-5 pb-4 border-b border-white/10">
        <div className="flex items-center gap-3 mb-5">
          {/* CSU Logo badge */}
          <div className="w-11 h-11 rounded-xl flex items-center justify-center flex-shrink-0"
            style={{ background: "#093d23" }}>
            <span className="text-sm font-bold" style={{ color: "#6abf69" }}>CS</span>
            <span className="text-sm font-bold text-white">U</span>
          </div>
          <div>
            <p className="text-xs text-white/60 leading-tight">Cleveland State</p>
            <p className="text-lg font-semibold leading-tight">VikingGPT</p>
          </div>
        </div>

        {/* New Chat button */}
        <button
          onClick={onNewChat}
          className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm font-medium transition-colors mb-2"
          style={{ background: "rgba(255,255,255,0.12)" }}
          onMouseOver={e => (e.currentTarget.style.background = "rgba(255,255,255,0.2)")}
          onMouseOut={e => (e.currentTarget.style.background = "rgba(255,255,255,0.12)")}
        >
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path fillRule="evenodd" d="M10 3a1 1 0 011 1v5h5a1 1 0 110 2h-5v5a1 1 0 11-2 0v-5H4a1 1 0 110-2h5V4a1 1 0 011-1z" clipRule="evenodd"/>
          </svg>
          New Chat
        </button>

        {/* Explore Agents link */}
        <button
          onClick={onNewChat}
          className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-white/80 transition-colors"
          onMouseOver={e => (e.currentTarget.style.background = "rgba(255,255,255,0.1)")}
          onMouseOut={e => (e.currentTarget.style.background = "transparent")}
        >
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16">
            <path d="M5 3a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2V5a2 2 0 00-2-2H5zM5 11a2 2 0 00-2 2v2a2 2 0 002 2h2a2 2 0 002-2v-2a2 2 0 00-2-2H5zM11 5a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V5zM11 13a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/>
          </svg>
          Explore Agents
        </button>
      </div>

      {/* Recent chat history */}
      <div className="flex-1 overflow-y-auto px-3 py-4">
        <p className="text-xs font-semibold text-white/40 uppercase tracking-wider px-2 mb-1">Chats</p>
        <p className="text-xs text-white/40 px-2 mb-3">Previous 7 days</p>
        {RECENT_CHATS.map((chat, i) => (
          <button
            key={i}
            onClick={() => onSelectAgent("Viking Chat")}
            className="flex items-center gap-2 w-full px-3 py-2 rounded-lg text-sm text-white/75 transition-colors text-left truncate mb-0.5"
            onMouseOver={e => (e.currentTarget.style.background = "rgba(255,255,255,0.1)")}
            onMouseOut={e => (e.currentTarget.style.background = "transparent")}
          >
            <svg viewBox="0 0 20 20" fill="currentColor" width="14" height="14" className="flex-shrink-0">
              <path fillRule="evenodd" d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7z" clipRule="evenodd"/>
            </svg>
            <span className="truncate">{chat}</span>
          </button>
        ))}
      </div>

      {/* History/Archived tabs + user profile */}
      <div className="border-t border-white/10">
        <div className="flex px-3 py-2 gap-1">
          <button className="flex-1 py-1.5 text-xs font-semibold rounded-lg text-white"
            style={{ background: "rgba(255,255,255,0.15)" }}>HISTORY</button>
          <button className="flex-1 py-1.5 text-xs text-white/50 rounded-lg">ARCHIVED</button>
        </div>
        <div className="flex items-center gap-3 px-4 py-3 border-t border-white/10">
          <div className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-semibold flex-shrink-0"
            style={{ background: "#6abf69", color: "#0d4f2e" }}>KP</div>
          <span className="text-sm text-white/80 truncate">Karicheti, Krishna Pry...</span>
        </div>
      </div>
    </aside>
  );
}
