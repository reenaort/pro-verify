import { defineConfig } from 'vite';
import { resolve } from 'path';

export default defineConfig({
  build: {
    rollupOptions: {
      input: {
        main: resolve(__dirname, 'index.html'),
        admin: resolve(__dirname, 'admin.html'),
        adminLogin: resolve(__dirname, 'admin-login.html'),
        adminUpload: resolve(__dirname, 'admin-upload.html'),
        adminCodes: resolve(__dirname, 'admin-codes.html'),
        adminDetails: resolve(__dirname, 'admin-details.html'),
        verify: resolve(__dirname, 'verify.html'),
      },
    },
  },
});
