import React, { useState } from 'react';
import MessageBubble from './MessageBubble';

interface ChatWindowProps {
  greeting: string;
  brandColor: string;
  onClose: () => void;
}

export default function ChatWindow({ greeting, brandColor, onClose }: ChatWindowProps) {
  const [input, setInput] = useState('');

  const handleSend = () => {
    // TODO component 2.4: wire this to POST /chat
    setInput('');
  };

  return (
    <div
      className="lq-chat-window"
      style={{
        width: '360px',
        height: '480px',
        borderRadius: '12px',
        boxShadow: '0 8px 30px rgba(0,0,0,0.2)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        backgroundColor: '#fff',
        boxSizing: 'border-box',
      }}
    >
      {/* Header */}
      <div
        className="lq-header"
        style={{
          backgroundColor: brandColor,
          color: '#fff',
          padding: '14px 16px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          flexShrink: 0,
        }}
      >
        <span style={{ fontWeight: 600, fontSize: '15px' }}>Assistant</span>
        <button
          className="lq-close-btn"
          onClick={onClose}
          aria-label="Close chat"
          style={{
            background: 'none',
            border: 'none',
            color: '#fff',
            cursor: 'pointer',
            padding: '2px',
            display: 'flex',
            alignItems: 'center',
            outline: 'none',
          }}
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        </button>
      </div>

      {/* Messages area */}
      <div
        className="lq-messages"
        style={{
          flex: 1,
          overflowY: 'auto',
          padding: '16px',
          display: 'flex',
          flexDirection: 'column',
          gap: '8px',
        }}
      >
        <MessageBubble role="assistant" content={greeting} brandColor={brandColor} />
      </div>

      {/* Input bar */}
      <div
        className="lq-input-bar"
        style={{
          borderTop: '1px solid #e5e5e5',
          padding: '10px 12px',
          display: 'flex',
          gap: '8px',
          flexShrink: 0,
        }}
      >
        <input
          className="lq-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') handleSend(); }}
          placeholder="Type a message..."
          style={{
            flex: 1,
            border: '1px solid #ddd',
            borderRadius: '8px',
            padding: '8px 12px',
            fontSize: '14px',
            outline: 'none',
            boxSizing: 'border-box',
            fontFamily: 'inherit',
          }}
        />
        <button
          className="lq-send-btn"
          onClick={handleSend}
          aria-label="Send message"
          style={{
            backgroundColor: brandColor,
            color: '#fff',
            border: 'none',
            borderRadius: '8px',
            padding: '8px 14px',
            cursor: 'pointer',
            fontSize: '14px',
            fontWeight: 600,
            outline: 'none',
            flexShrink: 0,
          }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
