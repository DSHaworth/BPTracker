<template>
    <md-dialog 
        :md-close-on-esc="false" 
        :md-fullscreen="false"
        :md-click-outside-to-close="false" 
        :md-active.sync="showDialog">
        <md-progress-bar md-mode="indeterminate"></md-progress-bar>        
        <div class="md-display-3 msg">{{msg}}</div>
    </md-dialog>
</template>

<script>
export default {
  name: 'LoadingDialog',
  props: {
    msg: String,
    showDialog: Boolean
  }
}    
</script>

<style scoped lang="scss">
  .msg{
      text-align: center;
      padding: 25px;
  }
</style>