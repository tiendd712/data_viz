<h1>Business Type & Customer Churn Rate</h1>

<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import Lineplot from "/Users/hy/StaDS/23-24 spring/data visualisation in data science/assignment/my-app/src/lib/components/lineplot.svelte";

    
    let data = [{"ARMS & ARMOUR":38.47,"ADVENTURING EQUIPMENT":27.83,"TOOLS & KITS":10.03,"POTIONS & SCROLLS":9.63,"ANIMALS & TRANSPORTATION":4.55,"JEWELRY":3.68,"SUMMONING DEVICE":2.92,"MUSICAL INSTRUMENT":2.89}];
    let showLineChart = false;
    let selectedType = null;

    const updateState = (type) => {
    selectedType = type;
    // 根据 selectedType 更新 showLineChart
    showLineChart = type !== null;
  };



    // Define the createTreemapChart function
    function createTreemapChart(data) {
      // Specify the chart’s dimensions.
      const width = 1000;
      const height = 800;
  
      // Specify the color scale.
      const color = d3.scaleOrdinal(data.children.map(d => d.name), d3.schemeTableau10);
  
      // Compute the layout.
      const root = d3.treemap()
        .tile(d3.treemapSquarify) // You can change the tiling method here
        .size([width, height])
        .padding(1)
        .round(true)(
        d3.hierarchy(data)
          .sum(d => d.value)
          .sort((a, b) => b.value - a.value)
      );
  
      // Create the SVG container.
      const svg = d3.create("svg")
        .attr("viewBox", [-60, -80, width + 120, height + 220]) 
        .attr("width", width+20)
        .attr("height", height)
        .attr("style", "max-width: 70%; height: auto; font: 10px sans-serif;");
  
      // Add a line under the treemap
      svg.append("line")
        .attr("x1", 0)
        .attr("y1", height+20)
        .attr("x2", width+40)
        .attr("y2", height+20)
        .attr("stroke", "black")
        .attr("stroke-width", 10);
  
      // Add a line on the left to connect to the baseline
      svg.append("line")
        .attr("x1", 0)
        .attr("y1", -40)
        .attr("x2", 0)
        .attr("y2", height+25)
        .attr("stroke", "black")
        .attr("stroke-width", 10);
      
      svg.append("line")
        .attr("x1", 0)
        .attr("y1", 5)
        .attr("x2", -40) // The same x-coordinate as the start point of the left line
        .attr("y2", -30) // Keep the same y-coordinate as the start point
        .attr("stroke", "black")
        .attr("stroke-width", 5);
  
      svg.append("line")
        .attr("x1", -40)
        .attr("y1", 10)
        .attr("x2", 0)
        .attr("y2", 10)
        .attr("stroke", "black")
        .attr("stroke-width", 5);
      
      // Add two circles as wheels
      const wheelRadius = 50;
      const wheelY = height + 75; // Distance below the line
  
      svg.append("circle")
        .attr("cx", wheelRadius * 2)
        .attr("cy", wheelY)
        .attr("r", wheelRadius)
        .attr("fill", "gray");
  
      svg.append("circle")
        .attr("cx", width - wheelRadius * 2)
        .attr("cy", wheelY)
        .attr("r", wheelRadius)
        .attr("fill", "gray");
  
      // Add a cell for each leaf of the hierarchy.
      const leaf = svg.selectAll("g")
        .data(root.leaves())
        .join("g")
        .attr("transform", d => `translate(${d.x0},${d.y0})`);
  
      // Append a tooltip.
      const format = d3.format(",d");
      leaf.append("title")
        .text(d => `${d.ancestors().reverse().map(d => d.data.name).join(".")}\n${format(d.value)}`);

      // Append a color rectangle.
      leaf.append("rect")
        .on("mouseover", (event, d) => {
          console.log(`Mouseover on ${d.data.name}`); 
          selectedType = d.data.name; // 更新当前悬停的类别名称
          showLineChart = true;
          console.log('Type:', selectedType); // 映射到 Type
      }) 
        .on("mouseout", () => {
          console.log('Mouseout event'); 
          selectedType = null; // 重置悬停的类别名称
          showLineChart = false;})
        .attr("id", d => (d.leafUid = document.createElementNS("http://www.w3.org/2000/svg", "clipPath")).id)
        .attr("fill", d => color(d.value))
        .attr("fill-opacity", 0.6)
        .attr("width", d => d.x1 - d.x0)
        .attr("height", d => d.y1 - d.y0);
        console.log('Type:', selectedType);

        

  
      // Append multiline text. The last line shows the value and has a specific formatting.
      leaf.append("text")
        .selectAll("tspan")
        .data(d => [d.data.name, format(d.value)])
        .join("tspan")
        .attr("x", 20) // Adjust x position
        .attr("y", (d, i) => i * 20 + 40) // Adjust y position and line spacing
        .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
        .attr("font-weight", (d, i, nodes) => i === nodes.length - 1 ? "bold" : null)
        .style("font-size", "12px") // Increase font size
        .text(d => d);
      
  
      // Return the SVG and color scales
      return { svg };}
  
  
    // Transform data into hierarchical structure
    const types = Object.keys(data[0]); // Extract the types
    const hierarchicalData = {
      name: "root",
      children: types.map(type => ({
        name: type,
        value: data[0][type]
      }))
    };
  
    // Create the treemap chart on mount
    let chart;
    onMount(() => {
      chart = createTreemapChart(hierarchicalData);
      // Append the SVG to the container div
      document.getElementById("chart-container").appendChild(chart.svg.node());
    });


</script>

<div id="chart-container">
  <svg width="1000" height="800"></svg>
  <div class:line-chart-container="{showLineChart}">
    <!-- 这里的样式将会根据 showLineChart 的值动态添加 -->
    {#if showLineChart && selectedType}
      <Lineplot Type="{selectedType}" />
    {/if}
  </div>
</div>
  