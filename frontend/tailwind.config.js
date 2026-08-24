/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        bg: '#F5F1E8',
        surface: '#FFFDF7',
        'border-soft': '#E0D9CC',
        'border-strong': '#1A1917',
        'text-primary': '#1A1917',
        'text-secondary': '#6B6459',
        'text-on-dark': '#F5F1E8',
        'accent-primary': '#D94F2B',
        'accent-secondary': '#7A8B3A',
        'accent-tertiary': '#B58B2C',
        success: '#4A7C59',
        warning: '#D08A1E',
        danger: '#B23A2E',
        'code-bg': '#2B2A26',
        'code-text': '#E8E4D8',
        selection: 'rgba(217, 79, 43, 0.3)',
        'focus-ring': '#7A8B3A',
      },
      fontFamily: {
        display: ['"Space Grotesk"', 'sans-serif'],
        sans: ['"Manrope"', 'sans-serif'],
        mono: ['"JetBrains Mono"', 'monospace'],
      },
      boxShadow: {
        brutal: '4px 4px 0 #1A1917',
        'brutal-sm': '2px 2px 0 #1A1917',
        'brutal-lg': '6px 6px 0 rgba(26,25,23,0.8)',
      },
      borderRadius: {
        card: '6px',
      },
      letterSpacing: {
        tightest: '-0.02em',
        label: '0.08em',
      },
    },
  },
  plugins: [],
};