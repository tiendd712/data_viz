<script>
  export let width = 100; 
  export let height = 100;
  export let Year;
</script>

<svg
  xmlns="http://www.w3.org/2000/svg"
  viewBox="0 0 24 24"
  width="{width}"
  height="{height}"
  fill="none"
  stroke="black"
  stroke-width="2"
  stroke-linecap="round"
  stroke-linejoin="round"
>
  <circle cx="9" cy="21" r="1" fill="pink"></circle>
  <circle cx="20" cy="21" r="1" fill="pink"></circle>
  <line x1="10" y1="21" x2="20" y2="21" stroke="black" stroke-width="2"></line> 
  <path
    d="M1 1h4l2.68 12.072a2 2 0 0 0 1.936 1.456h8.784a2 2 0 0 0 1.936-1.456L23 6H6"
    fill={Year === 2020 ? "yellow" : Year === 2021 ? "green" : "hotpink"}
  ></path>
  <line x1="5" y1="3" x2="9" y2="21" stroke="silver" stroke-width="2"></line> 
</svg>

<style>
  circle {
    stroke: #fff; /* White stroke color */
    stroke-width: 2; /* Moderate stroke width */
    opacity: 0.8; /* Partial transparency */
  }

  path {
    stroke: pink; /* Pink stroke color */
    stroke-width: 2; /* Moderate stroke width */
    opacity: 0.8; /* Partial transparency */
  }
  
  line {
    stroke: silver; /* Silver stroke color for lines */
    stroke-width: 2; /* Moderate stroke width */
    opacity: 0.8; /* Partial transparency */
  }
</style>
