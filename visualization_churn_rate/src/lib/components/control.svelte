<script>
  const years = [2019, 2020, 2021, 2022, 2023];
  export let selectedYear = "All";

</script>

<div class="row">
  <div class="col-12">
    <label for="Year-select">Select Year:</label>
    <select id="Year-select" class="select" bind:value={selectedYear}>
      <option value="All">All</option>
      {#each years as Year}
        <option value={Year}>{Year}</option>
      {/each}
    </select>
  </div>
</div>
