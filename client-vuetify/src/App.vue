<template>
  <v-app>

    <v-app-bar app color="deep-purple accent-4" dense dark>

      <v-toolbar-title>State Tracker</v-toolbar-title>

      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn text to="/">Home</v-btn>
        <v-btn text to="/about">About</v-btn>
        <v-btn text v-if="isLoggedIn" to="/userstats">Stats</v-btn>
      </v-toolbar-items>

      <v-menu v-if="$vuetify.breakpoint.smOnly">
        <template v-slot:activator="{ on }">
          <v-btn icon v-on="on">
            <v-icon>mdi-dots-vertical</v-icon>
          </v-btn>
        </template>

        <v-list>
          <v-list-item to="/">
            <v-list-item-title>Home</v-list-item-title>
          </v-list-item>
          <v-list-item to="/about">
            <v-list-item-title>About</v-list-item-title>
          </v-list-item>
          <v-list-item v-if="isLoggedIn" to="/userstats">
            <v-list-item-title>Stats</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>

    </v-app-bar>
    <user-password-dialog :showLogonDialog="showLogonDialog" v-on:close-logon="onCloseLogon" :successAction="successAction"/>
    <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" :color="snackbar.color" top>
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="yellow" text v-bind="attrs" @click="snackbar.show = false" >
          Close
        </v-btn>
      </template>
    </v-snackbar>
    <v-main>      
      <v-container fluid>
        <router-view/>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import { mapGetters  } from 'vuex'
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
    },
    menu: [
      { icon: "home", title: "Link A" },
      { icon: "info", title: "Link B" },
      { icon: "warning", title: "Link C" }
    ]    
  }),
  methods: {
    onCloseLogon: function(){
      this.showLogonDialog = false;
    }    
  },
  computed: {
    ...mapGetters(['isLoggedIn']),    
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
  .v-toolbar__title{
      margin-right: 1rem;
  }
</style>