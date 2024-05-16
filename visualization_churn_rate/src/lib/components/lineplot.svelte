<script>
  // Dependencies
  import { select } from "d3-selection";
  import { axisBottom, axisLeft } from "d3-axis";
  import { line } from "d3-shape";
  import { schemeTableau10 } from "d3-scale-chromatic";
  import { scaleLinear, scaleOrdinal } from "d3-scale";
  import { format } from "d3-format";
  import { onMount } from 'svelte';
    import { index } from "d3";


  // Properties
  export let Type;
  const Year = [2019, 2020, 2021, 2022, 2023];
  let lineChartData = [];
  let loading = true;
  let error = null;
  
  
  onMount(() => {
  console.log('Type:', Type);
});


  $: if (Type) {
  console.log(`Fetching data for Type: ${Type}`);
  fetch(`/data/orders_type_sorted.json?Type=${Type}`)
    .then(response => response.json())
    .then(data => {
      console.log('Fetched data:', data);
      lineChartData =data.filter(item => item.Type === Type);
      console.log('lineChartData:', lineChartData);
    })
    .catch(error => {
      console.error('Error fetching JSON data:', error);
    });
} else {
  console.log('No Type specified');
}



  // Dimensions
  const [height, width] = [600, 1200];
  console.log('Height:', height);
  const margin = { top: 50, right: 5, bottom: 55, left: 50 };
  console.log('Margin:', margin);
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;
  console.log('Inner Width:', innerWidth);
  console.log('Inner Height:', innerHeight);

  // Scales
  const xScale = scaleLinear().domain([0, 13]).range([0, innerWidth]);
  const yScale = scaleLinear().domain([-20, 20]).range([innerHeight, 0]);
  const cScale = scaleOrdinal(["pink", "green", "black","brown","grey"]).domain([2019, 2020, 2021,2022,2023]);

  console.log('cScale:',cScale)

  // Axes
  const xAxis = (node) => axisBottom(xScale).tickValues([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])(select(node));
  const yAxis = (node) => axisLeft(yScale)(select(node));

  // Line generator
  const lineGenerator = line()
    .x((d) => xScale(d.Month))
    .y((d) => yScale(d.CustomerChurnRate));

  function createLegend(svg, colors) {
    // 使用 D3.js 的 select 函数来选择图例的 SVG 容器
    const legend = select(svg)
      .selectAll('.legend-item')
      .data(colors.domain())
      .join('g')
      .attr('class', 'legend-item')
      .attr('transform', (d, i) => `translate(0, ${i * 20})`);

    legend.append('rect')
      .attr('x', 10)
      .attr('y', -9)
      .attr('width', 18)
      .attr('height', 18)
      .attr('fill', colors);

    legend.append('text')
      .attr('x', 34)
      .attr('y', 9)
      .text(d => d);
  }

</script>

<svg viewBox={"0 0 " + width + " " + height} style={"max-width: " + width + "px; margin: 0 auto;"}>
  <defs>
    <pattern id="gridPattern" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#ccc" stroke-width="0.5" />
    </pattern>
  </defs>

  <rect x="0" y="0" width="100%" height="100%" fill="url(#gridPattern)" />

  <g transform="translate({margin.left}, {margin.top})">
  {#if lineChartData.length > 0}
  {#each lineChartData as element}
  {console.log(`Rendering dot for year ${element.Year} and month ${element.Month}`)}
    <circle
      class="dot"
      cx={xScale(+element.Month)}
      cy={yScale(+element.CustomerChurnRate)}
      r="5"
      fill={cScale(element.Year)}
    >
      <title>{element.Year}</title>
    </circle>
  {/each}
{:else}
  <p>No data available</p>
{/if}

    <!-- Line Plot -->
    {#each Year as year}
    {console.log(`Rendering line for year ${year}`)}
    <path
      class="line line-{year}"
      d={lineGenerator(lineChartData.filter(d => d.Year === year))}
      fill="none"
      stroke={cScale(year)}
      stroke-width="2"
    ></path>
    {/each}  


    <!-- Axes -->
    <g use:xAxis transform="translate(0, {innerHeight})">
      <text class="axis-label" x={innerWidth / 2} y={margin.bottom - 18}>
        Month
      </text>
    </g>
    <g use:yAxis>
      <text
        class="axis-label"
        x={-innerHeight / 2}
        y={-margin.left + 18}
        transform="rotate(-90)"
      >
        Customer Churn Rate
      </text>
    </g>
    <!-- Labels -->
    <text class="title" x={innerWidth / 2} y={0}>Customer Churn Rate plot</text>
  </g>
</svg>

<svg>
  <g class="legend" transform="translate(10, 10)">
    {#each Year as year, index}
      <g class="legend-item" transform={`translate(0, ${20 * index})`}>
        <rect width="18" height="18" y="-9" fill={cScale(year)} />
        <text x="24" dy=".35em">{year}</text>
      </g>
    {/each}
  </g>
</svg>

  

<style>
  .dot {
    opacity: 0.8;
  }
  .axis-label {
    font-size: 1.75em;
    text-anchor: middle;
    vertical-align: bottom;
    fill: currentcolor;
  }
  .title {
    font-size: 2.25em;
    text-anchor: middle;
  }
  .line {
    fill: none;
    stroke-width: 2;
  }
</style>


