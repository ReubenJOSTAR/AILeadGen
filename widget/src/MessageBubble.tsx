import React from 'react';

interface MessageBubbleProps {
  role: 'user' | 'assistant';
  content: string;
  brandColor?: string;
}

export default function MessageBubble({ role, content, brandColor = '#534AB7' }: MessageBubbleProps) {
  const isUser = role === 'user';

  return (
    <div
      className={`lq-bubble-msg lq-bubble-${role}`}
      style={{
        alignSelf: isUser ? 'flex-end' : 'flex-start',
        maxWidth: '80%',
      }}
    >
      <div
        style={{
          backgroundColor: isUser ? brandColor : '#f0f0f0',
          color: isUser ? '#fff' : '#1a1a1a',
          padding: '10px 14px',
          borderRadius: isUser ? '16px 16px 4px 16px' : '16px 16px 16px 4px',
          fontSize: '14px',
          lineHeight: '1.45',
          wordBreak: 'break-word',
        }}
      >
        {content}
      </div>
    </div>
  );
}
