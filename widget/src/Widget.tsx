import React, { useState } from 'react';
import ChatWindow from './ChatWindow';

interface WidgetProps {
  widgetId: string;
  apiUrl: string;
  sessionId: string;
  greeting?: string;
  brandColor?: string;
}

const FONT_STACK = '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif';

export default function Widget({
  widgetId,
  apiUrl,
  sessionId,
  greeting = "Hi there! I'm here to help — what brings you to our site today?",
  brandColor = '#534AB7',
}: WidgetProps) {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div
      className="lq-root"
      style={{
        fontFamily: FONT_STACK,
        boxSizing: 'border-box',
        fontSize: '14px',
        lineHeight: '1.5',
      }}
    >
      {/* Chat window */}
      <div
        className="lq-window-wrapper"
        style={{
          position: 'fixed',
          bottom: '88px',
          right: '20px',
          zIndex: 999999,
          opacity: isOpen ? 1 : 0,
          transform: isOpen ? 'translateY(0) scale(1)' : 'translateY(12px) scale(0.95)',
          transition: 'opacity 180ms ease, transform 180ms ease',
          pointerEvents: isOpen ? 'auto' : 'none',
        }}
      >
        <ChatWindow
          greeting={greeting}
          brandColor={brandColor}
          onClose={() => setIsOpen(false)}
        />
      </div>

      {/* Bubble button */}
      <button
        className="lq-bubble"
        onClick={() => setIsOpen((o) => !o)}
        aria-label={isOpen ? 'Close chat' : 'Open chat'}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          zIndex: 999999,
          width: '56px',
          height: '56px',
          borderRadius: '50%',
          border: 'none',
          cursor: 'pointer',
          backgroundColor: brandColor,
          color: '#fff',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 4px 12px rgba(0,0,0,0.25)',
          transition: 'transform 180ms ease, background-color 180ms ease',
          transform: isOpen ? 'rotate(0deg)' : 'rotate(0deg)',
          outline: 'none',
          padding: 0,
        }}
      >
        {isOpen ? (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <line x1="18" y1="6" x2="6" y2="18" />
            <line x1="6" y1="6" x2="18" y2="18" />
          </svg>
        ) : (
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
          </svg>
        )}
      </button>
    </div>
  );
}
