<template>
  <v-dialog v-model="loading" persistent width="300">
    <v-card color="primary" dark>
      <v-card-text>
        <div class="card-content">
          {{msg}}
          <v-progress-linear indeterminate color="white" class="mb-0"></v-progress-linear>
        </div>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'LoadingDialog',
  props: {
    msg: String,
    loading: Boolean
  },
}    
</script>

<style scoped lang="scss">
  .card-content{
      text-align: center;
      padding: 25px 0;
  }
</style>