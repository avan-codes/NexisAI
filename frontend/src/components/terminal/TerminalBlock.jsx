import React, { useEffect, useState } from 'react';

export default function TerminalBlock({ lines, delay = 400 }) {
  const [visibleLines, setVisibleLines] = useState(0);

  useEffect(() => {
    if (visibleLines < lines.length) {
      const t = setTimeout(() => setVisibleLines((v) => v + 1), delay);
      return () => clearTimeout(t);
    }
  }, [visibleLines, lines.length, delay]);

  return (
    <div className="bg-code-bg border-2 border-border-strong shadow-brutal-lg p-5 rounded-card">
      {lines.slice(0, visibleLines).map((line, i) => (
        <p key={i} className="font-mono text-[14px] text-code-text leading-6">
          {line}
        </p>
      ))}
      {visibleLines < lines.length && <span className="terminal-caret" />}
    </div>
  );
}