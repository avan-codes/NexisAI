import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import AppLayout from '../layouts/AppLayout';
import { getExecutions } from '../api/executions';
import StatusBadge from '../components/ui/StatusBadge';
import Button from '../components/ui/Button';
import Pagination from '../components/ui/Pagination';

export default function ExecutionsList() {
  const [page, setPage] = useState(1);
  const [status, setStatus] = useState('');
  const { data, isLoading } = useQuery({
    queryKey: ['executions', { page, status }],
    queryFn: () => getExecutions({ page, limit: 20, status }),
  });

  return (
    <AppLayout>
      <div className="max-w-[1440px] mx-auto">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6 gap-4">
          <h2 className="text-2xl font-display font-bold">Workflows</h2>
          <div className="flex gap-3">
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              className="bg-surface border-2 border-border-strong rounded-none px-3 py-2 font-mono text-sm focus:outline-none focus:border-focus-ring"
            >
              <option value="">All</option>
              <option value="pending">Pending</option>
              <option value="running">Running</option>
              <option value="awaiting_approval">Awaiting Approval</option>
              <option value="succeeded">Succeeded</option>
              <option value="failed">Failed</option>
            </select>
          </div>
        </div>

        <div className="border-2 border-border-strong rounded-card overflow-hidden">
          <table className="w-full">
            <thead className="bg-border-strong text-text-on-dark uppercase text-[12px] tracking-label">
              <tr>
                <th className="p-4 text-left">Execution ID</th>
                <th className="p-4 text-left">Repo</th>
                <th className="p-4 text-left">Command</th>
                <th className="p-4 text-left">Status</th>
                <th className="p-4 text-left">Started</th>
                <th className="p-4 text-left">Duration</th>
                <th className="p-4 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {isLoading ? (
                <tr><td colSpan={7} className="p-4 text-center font-mono text-sm">Loading...</td></tr>
              ) : data?.data?.items?.map((exec) => (
                <tr key={exec._id} className="border-b border-dashed border-border-soft hover:bg-[#F0E9D8]">
                  <td className="p-4 font-mono text-sm">
                    <a href={`/executions/${exec._id}`} className="text-accent-primary hover:underline">#{exec._id.slice(-6)}</a>
                  </td>
                  <td className="p-4 font-mono text-sm">{exec.repo?.full_name}</td>
                  <td className="p-4 font-mono text-sm truncate max-w-[200px]">{exec.command?.text}</td>
                  <td className="p-4"><StatusBadge status={exec.status} /></td>
                  <td className="p-4 font-mono text-xs text-text-secondary">{new Date(exec.created_at).toLocaleString()}</td>
                  <td className="p-4 font-mono text-xs text-text-secondary">{exec.duration || '—'}</td>
                  <td className="p-4 flex gap-2">
                    <Button variant="ghost" size="icon" onClick={() => window.location.href = `/executions/${exec._id}`}>
                      <Eye size={14} />
                    </Button>
                    {exec.status === 'failed' && (
                      <Button variant="secondary" size="icon" onClick={() => retryExecution(exec._id)}>
                        <RefreshCw size={14} />
                      </Button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <Pagination page={page} totalPages={data?.data?.total_pages || 1} onPageChange={setPage} />
      </div>
    </AppLayout>
  );
}