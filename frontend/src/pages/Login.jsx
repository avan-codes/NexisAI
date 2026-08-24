import React from 'react';
import { useNavigate } from 'react-router-dom';
import Button from '../components/ui/Button';
import TerminalBlock from '../components/terminal/TerminalBlock';

export default function Login() {
  const navigate = useNavigate();
  const handleGitHubLogin = () => {
    window.location.href = '/api/v1/auth/github';
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-bg noise-bg p-4">
      <div className="w-full max-w-[480px]">
        <TerminalBlock lines={['nexis:~$ connect github', 'Authenticating...', 'Repository access granted', 'nexis:~$ ready']} />
        <Button onClick={handleGitHubLogin} className="w-full mt-6">
          Connect GitHub
        </Button>
      </div>
    </div>
  );
}