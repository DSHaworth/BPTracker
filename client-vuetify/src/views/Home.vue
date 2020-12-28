<template>
  <div class="home">
    
    <v-card :loading="loading" class="mx-auto">

      <template slot="progress">
        <v-progress-linear height="5" indeterminate></v-progress-linear>
      </template>

      <v-card-title>Users</v-card-title>
      <v-card-text>
        <template v-if="!loading">
          <template v-if="users.length">
            <template>
              <v-row justify="space-around">
                <template v-for="u in users">
                  <userLogonAvatar :user="u" :key="u.userId"></userLogonAvatar>
                </template>
              </v-row>
            </template>
          </template>    
          <template v-else>
            <span class="md-display-3">Currently no users</span>
          </template>
        </template>  

      </v-card-text>
      <v-card-actions style="display: flex; flex-flow: row wrap; justify-content: flex-end;">
        <div>
          <v-btn to="/NewUser" elevation="2" raised>
            Create Account
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
    <!-- <loading-dialog msg="Getting Records" v-bind:loading="loading" /> -->
  </div>
</template>

<script>
// @ is an alias to /src
import statTrackerService from '@/services/statTrackerService'
//import LoadingDialog from '@/components/LoadingDialog.vue'
import UserLogonAvatar from '@/components/UserLogonAvatar.vue'

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
            this.users = res.data;
          } 
          })
          .catch((error) => {
              alert(error);
          })
          .finally(() => {
            this.loading = false;
          });
        }
  },    
  components: {
    UserLogonAvatar
  },
  created() {
    this.getUsers();
    // this.loading = true;
    // setTimeout(this.getUsers, 3000);
  }  
}
</script>
