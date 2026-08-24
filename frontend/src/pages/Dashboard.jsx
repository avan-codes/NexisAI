import React from 'react';
import { useQuery } from '@tanstack/react-query';
import AppLayout from '../layouts/AppLayout';
import TerminalCommandBar from '../components/terminal/TerminalCommandBar';
import StatCard from '../components/dashboard/StatCard';
import LiveActivityFeed from '../components/dashboard/LiveActivityFeed';
import RecentPRs from '../components/dashboard/RecentPRs';
import { getRepos } from '../api/repos';
import { getExecutions } from '../api/executions';

export default function Dashboard() {
  const { data: repos } = useQuery({ queryKey: ['repos'], queryFn: () => getRepos() });
  const currentRepoId = repos?.data?.[0]?._id;

  const { data: executions } = useQuery({
    queryKey: ['executions', { limit: 10 }],
    queryFn: () => getExecutions({ limit: 10 }),
  });

  return (
    <AppLayout>
      <div className="max-w-[1440px] mx-auto space-y-8">
        <TerminalCommandBar repoId={currentRepoId} />

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <StatCard value="8" label="Steps Eliminated" footnote="vs manual workflow" />
          <StatCard value="2 min" label="Avg Delivery Time" footnote="vs 30 min manual" />
          <StatCard value="0" label="Context Switches" footnote="in a single flow" />
          <StatCard value="100%" label="Audit Score" footnote="full traceability" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          <div className="lg:col-span-7">
            <LiveActivityFeed executions={executions?.data?.items || []} />
          </div>
          <div className="lg:col-span-5">
            <RecentPRs />
          </div>
        </div>
      </div>
    </AppLayout>
  );
}