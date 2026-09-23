import { useState } from 'react'
import apiClient from '../api/client'

function Chat() {
  const [input, setInput] = useState('')
  const [messages, setMessages] = useState([]) // { role: 'user' | 'assistant', text }
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', text: input }
    setMessages((prev) => [...prev, userMessage]) // show the user's message right away
    setInput('')
    setLoading(true)

    try {
      const res = await apiClient.post('/chat/', { message: userMessage.text })
      setMessages((prev) => [...prev, { role: 'assistant', text: res.data.reply }])
    } catch {
      setMessages((prev) => [...prev, { role: 'assistant', text: 'Error: could not reach backend' }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto flex h-svh max-w-2xl flex-col p-4">
      <div className="flex-1 space-y-3 overflow-y-auto">
        {messages.map((m, i) => (
          <div
            key={i}
            className={`max-w-[75%] rounded-lg px-3 py-2 ${
              m.role === 'user' ? 'ml-auto bg-blue-600 text-white' : 'bg-gray-200 text-gray-900'
            }`}
          >
            {m.text}
          </div>
        ))}
        {loading && <div className="text-gray-400">thinking...</div>}
      </div>

      <div className="mt-4 flex gap-2">
        <input
          className="flex-1 rounded border px-3 py-2"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()} // Enter also sends
          placeholder="Type a message..."
        />
        <button onClick={sendMessage} className="rounded bg-blue-600 px-4 py-2 text-white">
          Send
        </button>
      </div>
    </div>
  )
}

export default Chat
