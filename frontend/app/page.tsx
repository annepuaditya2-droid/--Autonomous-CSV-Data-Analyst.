"use client";
import { useState } from "react";

// Define the type for our messages
interface Message {
  role: string;
  content: string;
  image?: string;
}

export default function Home() {
  const [input, setInput] = useState("");
  const [uploadStatus, setUploadStatus] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    { role: "assistant", content: "Welcome to StatBot Pro! 🚀 Please upload a CSV file in the sidebar to begin your analysis." }
  ]);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploadStatus("Uploading...");
    const formData = new FormData();
    formData.append("file", file);

    try {
        const res = await fetch("http://127.0.0.1:8000/upload", {
            method: "POST",
            body: formData,
        });
        const data = await res.json();
        
        if (data.status === "success") {
            setUploadStatus("✅ " + data.message);
            setMessages(prev => [...prev, { role: "assistant", content: `Data loaded successfully! I am ready to analyze **${file.name}**.` }]);
        } else {
            setUploadStatus("❌ Upload failed");
        }
    } catch (error) {
        setUploadStatus("🚨 Connection error");
    }
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
    
    const newMessages = [...messages, { role: "user", content: input }];
    setMessages(newMessages);
    setInput(""); 

    try {
        const res = await fetch("http://127.0.0.1:8000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: input })
        });
        
        const data = await res.json();
        
        if (data.status === "success") {
            setMessages([...newMessages, { 
                role: "assistant", 
                content: data.bot_answer,
                image: data.image_url 
            }]);
        } else {
            setMessages([...newMessages, { role: "assistant", content: "❌ Error: " + data.message }]);
        }
    } catch (error) {
        setMessages([...newMessages, { role: "assistant", content: "🚨 Cannot connect to Python backend." }]);
    }
  };

  return (
    <div className="flex h-screen bg-[#0f0f0f] text-gray-200">
      {/* ⬛ SIDEBAR */}
      <div className="w-72 bg-[#171717] p-5 hidden md:flex flex-col border-r border-gray-800 shadow-xl z-10">
        
        {/* Awesome Gradient Brand Heading */}
        <h1 className="text-3xl font-extrabold mb-10 bg-clip-text text-transparent bg-gradient-to-r from-blue-400 to-emerald-400 tracking-tight">
          StatBot Pro
        </h1>
        
        <h2 className="text-xs text-gray-500 mb-3 font-bold uppercase tracking-widest">Workspace</h2>
        <button className="text-left w-full bg-[#262626] hover:bg-[#333333] p-3 rounded-xl transition flex items-center gap-3 mb-10 font-medium shadow-sm border border-gray-700">
          <span className="text-lg">📝</span> New Chat
        </button>

        <h2 className="text-xs text-gray-500 mb-3 font-bold uppercase tracking-widest">Data Source</h2>
        <label className="cursor-pointer bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-500 hover:to-blue-600 text-white text-sm font-semibold py-3 px-4 rounded-xl transition block text-center shadow-lg transform hover:-translate-y-0.5">
          📂 Upload CSV
          <input type="file" accept=".csv" className="hidden" onChange={handleFileUpload} />
        </label>
        {uploadStatus && <div className="text-xs font-medium text-gray-400 mt-4 text-center bg-[#262626] p-2 rounded-lg">{uploadStatus}</div>}
      </div>

      {/* ⬛ MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col relative bg-[#0f0f0f]">
        
        {/* Top Header Area */}
        <div className="p-5 border-b border-gray-800 flex justify-between items-center bg-[#171717]/90 backdrop-blur-md sticky top-0 z-10">
          <h2 className="text-xl font-semibold text-gray-200 tracking-wide">Analytics Engine</h2>
          <div className="flex items-center gap-2">
            <span className="flex h-3 w-3">
              <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
            </span>
            <span className="text-xs font-medium text-gray-400">System Online</span>
          </div>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto p-6 space-y-8 pb-40 scroll-smooth">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-4xl p-5 rounded-2xl shadow-lg ${
                msg.role === 'user' 
                  ? 'bg-blue-600 text-white rounded-tr-sm' 
                  : 'bg-[#212121] text-gray-200 border border-gray-800 rounded-tl-sm'
              }`}>
                <span className={`font-bold text-xs block mb-3 uppercase tracking-wider ${msg.role === 'user' ? 'text-blue-200' : 'text-gray-400'}`}>
                  {msg.role === 'user' ? 'You' : 'StatBot AI'}
                </span>
                
                <div className="whitespace-pre-wrap leading-relaxed text-[15px] font-medium">
                  {msg.content}
                </div>

                {/* The Image Viewer */}
                {msg.image && (
                  <div className="mt-5 p-2 bg-white rounded-xl shadow-inner inline-block">
                    <img 
                      src={msg.image} 
                      alt="Generated Chart" 
                      className="rounded-lg max-w-full h-auto object-contain"
                    />
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input Box Area */}
        <div className="absolute bottom-0 w-full p-6 bg-gradient-to-t from-[#0f0f0f] via-[#0f0f0f] to-transparent">
          <div className="max-w-4xl mx-auto flex items-center bg-[#212121] rounded-full px-6 py-4 shadow-2xl border border-gray-700 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
            <input 
              type="text" 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
              placeholder="Ask a complex data question..." 
              className="flex-1 bg-transparent outline-none text-white placeholder-gray-500 text-lg font-medium"
            />
            <button 
              onClick={sendMessage} 
              className="ml-4 p-3 bg-white text-black rounded-full hover:bg-blue-500 hover:text-white transition-colors shadow-md flex items-center justify-center"
            >
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
                <path strokeLinecap="round" strokeLinejoin="round" d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" />
              </svg>
            </button>
          </div>
          <div className="text-center text-xs text-gray-500 mt-4 font-medium">
            StatBot Pro can make mistakes. Always verify critical business data.
          </div>
        </div>
      </div>
    </div>
  );
}