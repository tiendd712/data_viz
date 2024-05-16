<script>
import { onMount } from 'svelte';
import * as d3 from 'd3';

export let hoverData;
  
  onMount(() => {
    const width = 400;
    const height = 200;
    const types = ["ARMS & ARMOUR", "ADVENTURING EQUIPMENT", "TOOLS & KITS", "POTIONS & SCROLLS", "ANIMALS & TRANSPORTATION", "JEWELRY", "SUMMONING DEVICE", "MUSICAL INSTRUMENT"];
    const color = d3.scaleOrdinal(types, d3.schemeTableau10);
  
  const root = d3.treemap()
    .tile(d3.treemapSquarify)
    .size([width, height])
    .padding(1)
    .round(true)(
      d3.hierarchy(hoverData)
        .sum(d => d.value)
        .sort((a, b) => b.value - a.value)
    );

  const svg = d3.select("#Treemap-container")
    .append("svg")
    .attr("viewBox", [-20, -50, width + 40, height + 150]) 
    .attr("width", width)
    .attr("height", height)
    .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");

  const leaf = svg.selectAll("g")
    .data(root.leaves())
    .join("g")
    .attr("transform", d => `translate(${d.x0},${d.y0})`);

  const format = d3.format(",d");
  leaf.append("title")
    .text(d => `${d.ancestors().reverse().map(d => d.data.name).join(".")}\n${format(d.value)}`);

  leaf.append("rect")
    .attr("fill", d => color(d.data.name))
    .attr("fill-opacity", 0.6)
    .attr("width", d => d.x1 - d.x0)
    .attr("height", d => d.y1 - d.y0);

  leaf.append("text")
    .selectAll("tspan")
    .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g).concat(format(d.value)))
    .join("tspan")
    .attr("x", 3)
    .attr("y", (d, i, nodes) => `${(i === nodes.length - 1 ? 1 : 0.3) + 1.1 + i * 0.9}em`)
    .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
    .style("font-size", "5px") 
    .text(d => d);
});
