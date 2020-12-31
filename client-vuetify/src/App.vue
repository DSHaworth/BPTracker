<template>
  <v-app>
    <v-main>      
      <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </div>
      <user-password-dialog :showLogonDialog="showLogonDialog" v-on:close-logon="onCloseLogon" :successAction="successAction"/>
      <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" :color="snackbar.color" top>
        {{ snackbar.text }}
        <template v-slot:action="{ attrs }">
          <v-btn color="yellow" text v-bind="attrs" @click="snackbar.show = false" >
            Close
          </v-btn>
        </template>
      </v-snackbar>
      <div class="router-view">
        <router-view/>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import UserPasswordDialog from '@/components/UserPasswordDialog.vue'
import EventBus from '@/eventBus'

export default {
  name: 'App',
  components: {
    UserPasswordDialog,
  },
  data: () => ({
    showLogonDialog: false,
    successAction: null,
    snackbar: {
      show: false,
      // text: "",
      // timeout: 3000,
      // color: ""
    },      
  }),
  methods: {
    onCloseLogon: function(){
      this.showLogonDialog = false;
    }    
  },
  mounted () {
    EventBus.$on('REAUTHENTICATE', (payload) => {
      this.successAction = payload;
      this.showLogonDialog = true;
    }),
    EventBus.$on('SNACKBAR', (payload) => {
      this.snackbar = payload;
    })
  }  
};
</script>

<style scoped lang="scss">
  .router-view{
      padding: .5rem;
  }
</style>