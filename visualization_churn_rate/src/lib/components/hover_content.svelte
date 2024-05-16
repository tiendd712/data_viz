<script>
    import { onMount } from 'svelte';
    import * as d3 from 'd3';
    import Tooltip from '/Users/hy/my-app/src/lib/components/Tooltip.svelte';
    import { tooltipContent } from '../../stores/tooltipStore.js';


    let jsonData = null;

    import('/Users/hy/my-app/static/data/orders_type.json').then(module => {
    jsonData = module.default;
  });

  function convertToTreemapData(data) {
    const treemapData = {
      name: `${data.Year}-${data.Month}`,
      children: Object.keys(data)
        .filter(key => key.startsWith('ADVENTURING EQUIPMENT_') || key.startsWith('TOOLS & KITS_') || key.startsWith('POTIONS & SCROLLS_') || key.startsWith('ANIMALS & TRANSPORTATION_') || key.startsWith('JEWELRY_') || key.startsWith('SUMMONING DEVICE_') || key.startsWith('MUSICAL INSTRUMENT_'))
        .map(key => {
          const category = key.replace('_Percentage', '');
          return {
            name: category,
            value: data[key]
          };
        })
    };
    return treemapData;
  }
  
    // Define the createTreemapChart function
    function createTreemapChart(data) {
      // Specify the chart’s dimensions.
      const width = 400;
      const height = 200;
  
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
              .attr("viewBox", [-20, -50, width + 40, height + 150]) 
        .attr("width", width)
        .attr("height", height)
              .attr("style", "max-width: 100%; height: auto; font: 10px sans-serif;");
  
      // Add a line under the treemap
      svg.append("line")
        .attr("x1", 0)
        .attr("y1", height+20)
        .attr("x2", width)
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
        .attr("stroke-width", 5);
          
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
  
      const wheelRadius = 30;
      const wheelY = height + 55; // Distance below the line
  
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
        .attr("id", d => (d.leafUid = document.createElementNS("http://www.w3.org/2000/svg", "clipPath")).id)
        .attr("fill", d => color(d.value))
        .attr("fill-opacity", 0.6)
        .attr("width", d => d.x1 - d.x0)
        .attr("height", d => d.y1 - d.y0);
  
      // Append a clipPath to ensure text does not overflow.
      leaf.append("clipPath")
        .attr("id", d => (d.clipUid = document.createElementNS("http://www.w3.org/2000/svg", "clipPath")).id)
        .append("use")
        .attr("xlink:href", d => d.leafUid.href);
  
      // Append multiline text. The last line shows the value and has a specific formatting.
      leaf.append("text")
        .attr("clip-path", d => d.clipUid)
        .selectAll("tspan")
        .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g).concat(format(d.value)))
        .join("tspan")
        .attr("x", 3)
        .attr("y", (d, i, nodes) => `${(i === nodes.length - 1) * 0.3 + 1.1 + i * 0.9}em`)
        .attr("fill-opacity", (d, i, nodes) => i === nodes.length - 1 ? 0.7 : null)
              .style("font-size", "5px") 
        .text(d => d);
   

      // Return the SVG and color scales
      return { svg };
    }

    let Year=2019;
    let Month=1;

    const chartDescription = `${Year}-${Month}`;
      
    async function loadTreemapData() {
    if (jsonData && jsonData.length > 0) {
      const treemapData = convertToTreemapData(jsonData[0]);
      const treemapChart = createTreemapChart(treemapData);
      tooltipContent = treemapChart.svg.node().outerHTML;
    }
  }

  onMount(() => {
    loadTreemapData();
  });

  function handleHover(dataPoint) {
  const treemapData = convertToTreemapData(dataPoint);
  const treemapChartSvg = createTreemapChart(treemapData);
  tooltipContent.set(treemapChartSvg.svg.node().outerHTML); // 更新 tooltipContent
}

  function handleFocus(dataPoint){
    handleHover(dataPoint);
  }

  function handleBlur() {
  tooltipContent = '';
}
</script>

<Tooltip content={$tooltipContent} />


<div>
  {#if $jsonData}
    {#await createTreemapChart($jsonData[0])}
      <p>Loading...</p>
    {:then svg}
    <div innerHTML={svg} />
    {/await}
  {/if}
</div>

<!-- Assuming you have a scatterplot component -->
<shoppingcartplot
  role="img"
  aria-label={`Shopping cart plot for ${chartDescription}`}
  on:mouseover={(event) => handleHover(event.detail)}
  on:focus={(event) => handleFocus(event.detail)}
  on:blur={(event) => handleBlur()}
/>