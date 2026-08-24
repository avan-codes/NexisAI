import { useEffect, useRef } from 'react';
import { useAuthStore } from '../store/auth';

export default function useWebSocket(url, onMessage) {
  const token = useAuthStore((s) => s.token);
  const wsRef = useRef(null);

  useEffect(() => {
    if (!token) return;
    const ws = new WebSocket(`${url}?token=${token}`);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      onMessage(data);
    };

    ws.onerror = (error) => console.error('WebSocket error:', error);

    return () => {
      ws.close();
      wsRef.current = null;
    };
  }, [url, token]);

  return wsRef;
}