<template>
  <v-dialog v-model="showLogonDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">User Profile</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-row>
            <v-col cols="12">
              <v-text-field label="Password*" type="password" required></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog()">
          Close
        </v-btn>
        <v-btn color="blue darken-1" text @click="authenticate()">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
export default {
  name: 'UserPasswordDialog',
  props: {
    showLogonDialog: Boolean
  },
  data(){
    return {
      isOpen: this.showLogonDialog
    }
  },
  methods: {
    closeDialog: function(){
      this.showLogonDialog = this.isOpen = false;
    },
    authenticate: function(){
      alert("Auth this user");
      this.showLogonDialog = this.isOpen = false;
    }
  }
}    
</script>