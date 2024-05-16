import { writable } from 'svelte/store';

export const tooltipContent = writable({
  content: '',
  dataPoint: null,
  show: false
});