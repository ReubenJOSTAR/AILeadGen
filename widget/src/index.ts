import React from 'react';
import { createRoot } from 'react-dom/client';
import Widget from './Widget';

(function () {
  const script = document.currentScript as HTMLScriptElement;
  const widgetId = script?.getAttribute('data-widget-id') || '';
  const apiUrl = script?.getAttribute('data-api-url') || '';

  if (!widgetId) {
    console.error('[LeadQualify] Missing data-widget-id attribute on script tag');
    return;
  }

  const SESSION_KEY = 'lq_session_id';
  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, sessionId);
  }

  const root = document.createElement('div');
  root.id = 'lq-widget-root';
  document.body.appendChild(root);

  createRoot(root).render(
    React.createElement(Widget, { widgetId, apiUrl, sessionId })
  );
})();
