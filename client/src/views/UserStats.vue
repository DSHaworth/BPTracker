<template>  
  <div class="container">
    <md-tabs>
      <md-tab id="tab-weight" md-label="Weight">
        <div>Here is my weight</div>
      </md-tab>
      <md-tab id="tab-pulse" md-label="Pulse">
        <div>Here is my pulse</div>
      </md-tab>
      <md-tab id="tab-bloodpressure" md-label="BP">
          <div>Blood Pressure</div>
      </md-tab>
    </md-tabs>
  </div>
</template>

<script>
  export default {
    name: 'UserStats'
  }
</script>

<style lang="scss" scoped>
.container {
    padding: 2rem;
}
</style>