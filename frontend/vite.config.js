import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  server: {
    host:true,
    port: 3000, // <-- Escribe aquí el puerto que deseas usar
    strictPort: true, // Si es true, Vite dará error si el puerto está ocupado en lugar de saltar a otro
  }
})
