<!-- Tooltip.svelte -->
<script>
  import { onMount } from 'svelte';
  import {tooltipContent} from '/Users/hy/my-app/src/stores/tooltipStore.js'; // 引入 tooltipContent store

  let content = ''; // 初始化 content

  // 使用 onMount 钩子订阅 tooltipContent 的变化
  onMount(() => {
    const unsubscribe = tooltipContent.subscribe(value => {
      content = value;
    });

    // 当组件销毁时取消订阅
    return unsubscribe;
  });
</script>

{#if content}
  <div class="tooltip">
    {@html content} <!-- 使用 {@html} 来渲染 HTML/SVG 字符串 -->
  </div>
{/if}

<style>
  /* 样式定义... */
</style>
