import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
      '/docs': 'http://localhost:5000',
      '/redoc': 'http://localhost:5000',
      '/openapi.json': 'http://localhost:5000',
    },
  },
})
