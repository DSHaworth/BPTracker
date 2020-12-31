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
                  <userLogonAvatar :user="u" :key="u.userId" v-on:selected-user="onSelectedUser"></userLogonAvatar>
                </template>
              </v-row>
            </template>
          </template>    
          <template v-else>
            <span class="md-display-3">Currently no users</span>
          </template>
        </template>  

      </v-card-text>
      <v-card-actions class="right-side">
        <div>
          <v-btn @click="onShowCreate" elevation="2" raised>
            Create Account
          </v-btn>
        </div>
      </v-card-actions>
    </v-card>
    <!-- <loading-dialog msg="Getting Records" v-bind:loading="loading" /> -->
    <user-create-dialog :showCreateDialog="showCreateDialog" v-on:close-create="onCloseCreate"/>
  </div>
</template>

<script>
// @ is an alias to /src
import statTrackerService from '@/services/statTrackerService'
import UserLogonAvatar from '@/components/UserLogonAvatar.vue'
import UserCreateDialog from '@/components/UserCreateDialog.vue'
import EventBus from '@/eventBus'

export default {
  name: 'Home',
  data() { 
    return {
      loading: false,
      showCreateDialog: false,
      users: []
    }
  },
  computed:{    
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
    },
    onSelectedUser: function(user){

      this.$store.dispatch('logout');
      this.$store.dispatch('setUser', user);

      EventBus.$emit('REAUTHENTICATE', '/UserStats')
    },
    // Create User
    onShowCreate: function(){
      this.showCreateDialog = true;
    },
    onCloseCreate: function(){
      this.showCreateDialog = false;
      this.getUsers();
    }
  },    
  components: {
    UserLogonAvatar,
    UserCreateDialog
  },
  created() {
    this.getUsers();
  }  
}
</script>
