import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
  // 服务器配置
  server: {
    fs: {
      // 允许从项目根目录下的 static 目录提供文件
      allow: ['static']
    }
  },
  // 插件列表
  plugins: [sveltekit()]
});