// =============================================
// Agent Cards — Home View
// Shows the official VikingGPT agents grid
// Matches BearcatGPT's Official Agents layout
// =============================================

"use client";

type Props = { onSelectAgent: (name: string) => void };

const AGENTS = [
  {
    name: "Viking Chat",
    desc: "I am VikingGPT, an AI assistant that searches csuohio.edu in real-time to answer any question about Cleveland State University.",
    icon: (
      <svg viewBox="0 0 40 40" fill="none" width="24" height="24">
        <path d="M8 32 L20 8 L32 32 Z" fill="#6abf69"/>
        <circle cx="20" cy="25" r="5" fill="white"/>
      </svg>
    ),
  },
  {
    name: "CSU Admissions",
    desc: "Get step-by-step help with applications, deadlines, transfer requirements, and graduate admissions at Cleveland State.",
    icon: (
      <svg viewBox="0 0 40 40" fill="none" width="24" height="24">
        <rect x="7" y="13" width="26" height="19" rx="2" fill="#6abf69"/>
        <path d="M14 13V11a6 6 0 0112 0v2" stroke="white" strokeWidth="2.2"/>
        <rect x="15" y="22" width="10" height="2" rx="1" fill="white"/>
      </svg>
    ),
  },
  {
    name: "Campus Resources",
    desc: "Find rec center hours, library access, tutoring, counseling, parking, dining, and all CSU student services.",
    icon: (
      <svg viewBox="0 0 40 40" fill="none" width="24" height="24">
        <circle cx="20" cy="20" r="12" fill="none" stroke="#6abf69" strokeWidth="2.5"/>
        <path d="M20 14v6l4 3" stroke="#6abf69" strokeWidth="2" strokeLinecap="round"/>
      </svg>
    ),
  },
];

export default function AgentCards({ onSelectAgent }: Props) {
  return (
    <div className="flex flex-col h-full overflow-y-auto">
      {/* Header */}
      <div className="px-8 pt-8 pb-6 border-b border-gray-100">
        <h1 className="text-2xl font-semibold text-gray-900 mb-4">VikingGPT</h1>
        <div className="flex items-center gap-3 bg-gray-50 border border-gray-200 rounded-2xl px-4 py-2.5 max-w-md">
          <svg viewBox="0 0 20 20" fill="currentColor" width="16" height="16" className="text-gray-400">
            <path fillRule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clipRule="evenodd"/>
          </svg>
          <input type="text" placeholder="Search for an Agent" className="bg-transparent flex-1 text-sm outline-none text-gray-700 placeholder-gray-400"/>
        </div>
      </div>

      {/* Official Agents section */}
      <div className="px-8 py-6">
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-base font-semibold text-gray-900">Official Agents</h2>
            <p className="text-xs text-gray-500 mt-0.5">Engineered with permissions and safeguards for secure and controlled access</p>
          </div>
          <a href="#" className="text-sm font-medium" style={{ color: "#0d4f2e" }}>Browse all agents</a>
        </div>

        {/* Cards grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {AGENTS.map(agent => (
            <button
              key={agent.name}
              onClick={() => onSelectAgent(agent.name)}
              className="text-left bg-white border border-gray-200 rounded-xl p-4 hover:border-green-700 hover:shadow-sm transition-all"
            >
              <div className="flex items-center gap-3 mb-3">
                {/* CSU green icon with verified badge */}
                <div className="relative w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0"
                  style={{ background: "#0d4f2e" }}>
                  {agent.icon}
                  <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-green-500 rounded-full border-2 border-white flex items-center justify-center">
                    <svg viewBox="0 0 8 8" fill="none" width="8" height="8">
                      <path d="M1.5 4l2 2 3-3" stroke="white" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
                    </svg>
                  </div>
                </div>
                <span className="font-semibold text-sm text-gray-900">{agent.name}</span>
              </div>
              <p className="text-xs text-gray-500 leading-relaxed">{agent.desc}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
