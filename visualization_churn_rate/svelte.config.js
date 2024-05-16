import adapter from '@sveltejs/adapter-node';

export default {
  kit: {
    adapter: adapter(),
    // 如果应用部署在子路径下，可以设置 paths.base
    // paths: {
    //   base: '/my-app'
    // },
  },
  // Vite 配置应放在顶层，而不是 kit 对象内
  vite: {
    // 这里可以放置全局 Vite 配置
    // 例如，如果你需要自定义 Vite 配置，可以放在这里
  },
};