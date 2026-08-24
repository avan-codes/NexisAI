import React from 'react';
import Card from '../ui/Card';

export default function StatCard({ value, label, footnote }) {
  return (
    <Card className="p-6">
      <p className="font-display font-bold text-[32px] leading-10 text-text-primary">{value}</p>
      <p className="mt-1 font-sans uppercase text-[11px] tracking-label text-text-secondary">{label}</p>
      <p className="mt-2 font-mono text-[11px] text-text-secondary/70">{footnote}</p>
    </Card>
  );
}