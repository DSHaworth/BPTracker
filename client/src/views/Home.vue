<template>
  <div class="home">
    
    <div class="md-display-4">StatTrack</div>
    
    <template v-if="!loading">
      <template v-if="users.length">
        <template v-for="u in users">
          <userSelect :user="u" :key="u.userId"></userSelect>
        </template>
      </template>    
      <template v-else>
        <span class="md-display-3">Currently no users</span>
      </template>
      <div><md-button class="md-raised md-primary">Create Account</md-button></div>
    </template>   

    <loading-dialog msg="Getting Records" v-bind:showDialog="loading" />

  </div>
</template>

<script>
// @ is an alias to /src
import UserSelect from '@/components/UserSelect.vue'
import LoadingDialog from '@/components/LoadingDialog.vue'
import statTrackerService from '@/services/statTrackerService'

export default {
  name: 'Home',
  data() { 
    return {
      loading: false,
      users: []
    }
  },
  methods: {
    getUsers: function(){
      this.loading = true;
      statTrackerService.getUsers()      
        .then((res) => {
          if(res.data.isValid){
            console.log(res.data)
            this.users = res.data.payload;
          } else {
            console.log("Error")
            console.log(res);
            console.log(res.data.errorMessage);
          }
          })
          .catch((error) => {
              console.error(error);
          })
          .finally(() => {
            this.loading = false;
          });
        }
  },
  components: {
    UserSelect,
    LoadingDialog
  },
  created() {
    this.getUsers();
    // this.loading = true;
    // setTimeout(this.getUsers, 10000);
  }
}
</script>

<style lang="scss" scoped>

</style>