nexisai-frontend/
├── public/
│   ├── favicon.svg
│   ├── noise.png                 # subtle texture overlay (optional)
│   └── robots.txt
├── src/
│   ├── assets/
│   │   └── fonts/                # local font files (Space Grotesk, Manrope, JetBrains Mono)
│   │       ├── SpaceGrotesk-Variable.ttf
│   │       ├── Manrope-Variable.ttf
│   │       └── JetBrainsMono-Variable.ttf
│   ├── api/
│   │   ├── client.js             # Axios instance with JWT interceptors
│   │   ├── auth.js               # GitHub OAuth flow helpers
│   │   ├── commands.js           # command endpoints
│   │   ├── executions.js         # execution endpoints
│   │   ├── logs.js               # audit logs endpoints
│   │   ├── repos.js              # repository endpoints
│   │   └── settings.js           # settings endpoints
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.jsx
│   │   │   ├── Card.jsx
│   │   │   ├── Input.jsx
│   │   │   ├── Textarea.jsx
│   │   │   ├── StatusBadge.jsx
│   │   │   ├── Skeleton.jsx
│   │   │   ├── Modal.jsx
│   │   │   ├── Toast.jsx
│   │   │   ├── Pagination.jsx
│   │   │   ├── EmptyState.jsx
│   │   │   └── DiffViewer.jsx
│   │   ├── layout/
│   │   │   ├── Sidebar.jsx
│   │   │   ├── Topbar.jsx
│   │   │   └── CommandPalette.jsx
│   │   ├── execution/
│   │   │   ├── ExecutionTimeline.jsx
│   │   │   ├── StepNode.jsx
│   │   │   ├── StepLogs.jsx
│   │   │   ├── ApprovalCard.jsx
│   │   │   ├── PRCard.jsx
│   │   │   └── DeployCard.jsx
│   │   ├── dashboard/
│   │   │   ├── StatCard.jsx
│   │   │   ├── LiveActivityFeed.jsx
│   │   │   └── RecentPRs.jsx
│   │   └── terminal/
│   │       ├── TerminalCommandBar.jsx
│   │       └── TerminalBlock.jsx
│   ├── hooks/
│   │   ├── useWebSocket.js
│   │   ├── useDebounce.js
│   │   ├── useLocalStorage.js
│   │   └── useKeyboardShortcut.js
│   ├── layouts/
│   │   └── AppLayout.jsx
│   ├── pages/
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── ExecutionsList.jsx
│   │   ├── ExecutionDetail.jsx
│   │   ├── AuditLogs.jsx
│   │   ├── Settings.jsx
│   │   └── AuthCallback.jsx
│   ├── router/
│   │   ├── index.jsx
│   │   ├── ProtectedRoute.jsx
│   │   └── routes.js
│   ├── store/
│   │   ├── auth.js               # Zustand: user session
│   │   ├── execution.js          # Zustand: live execution state
│   │   ├── commandPalette.js     # Zustand: palette open/close
│   │   └── toasts.js             # Zustand: toast queue
│   ├── styles/
│   │   ├── fonts.css
│   │   ├── globals.css           # import fonts, base styles, utilities
│   │   └── noise.css             # optional texture
│   ├── utils/
│   │   ├── constants.js          # color tokens (if not in Tailwind)
│   │   ├── formatters.js         # date, duration, diff formatting
│   │   ├── validators.js         # command parsing helpers (frontend)
│   │   └── storage.js            # localStorage wrappers
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css                 # entry CSS (imports globals)
├── .env.example
├── .gitignore
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── index.html