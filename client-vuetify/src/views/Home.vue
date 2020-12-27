<template>
  <div class="home">
    
    <v-card :loading="loading" class="mx-auto my-12" max-width="374">

      <template slot="progress">
        <v-progress-linear color="deep-purple" height="10" indeterminate></v-progress-linear>
      </template>

      <v-card-title>Users</v-card-title>

    </v-card>
  
    
    <template v-if="!loading">
      <template v-if="users.length">
        <pre><code>{{users}}</code></pre>
        <!-- <template v-for="u in users">
          <userSelect :user="u" :key="u.userId"></userSelect>
        </template> -->
      </template>    
      <template v-else>
        <span class="md-display-3">Currently no users</span>
      </template>
      <div><md-button to="/NewUser" class="md-raised md-primary">Create Account</md-button></div>
    </template>  

  <loading-dialog msg="Getting Records" v-bind:loading="loading" />

  </div>
</template>

<script>
// @ is an alias to /src
import statTrackerService from '@/services/statTrackerService'
import LoadingDialog from '@/components/LoadingDialog.vue'

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
          if(res.data){
            console.log(res.data)
            this.users = res.data;
          } 
          })
          .catch((error) => {
              console.error(error);
              alert(error);
          })
          .finally(() => {
            this.loading = false;
          });
        }
  },    
  components: {
    LoadingDialog
  },
  created() {
    //this.getUsers();
    this.loading = true;
    setTimeout(this.getUsers, 3000);
  }  
}
</script>
