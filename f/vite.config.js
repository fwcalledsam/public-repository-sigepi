import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// <-- Despliegue en local -->
const FLASK_BACKEND_URL = 'http://127.0.0.1:5000'
const VITE_FRONTEND_PORT = 5173

export default defineConfig({
  plugins: [vue()],
  server: {
    host: '0.0.0.0',
    port: VITE_FRONTEND_PORT,
    proxy: {
      '/api': {
        target: FLASK_BACKEND_URL,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})

// <-- Despliegue en docker -->
// const FLASK_BACKEND_URL = process.env.BACKEND_API || 'http://localhost:5000'
// const VITE_FRONTEND_PORT = 5173

// export default defineConfig({
//   plugins: [vue()],
//   server: {
//     host: '0.0.0.0',
//     port: VITE_FRONTEND_PORT,
//     proxy: {
//       '/api': {
//         target: FLASK_BACKEND_URL,
//         changeOrigin: true,
//         secure: false,
//         rewrite: (path) => path.replace(/^\/api/, '')
//       }
//     }
//   },
// })