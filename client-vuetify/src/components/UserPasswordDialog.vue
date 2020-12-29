<template>
  <v-dialog v-if="user" v-model="showLogonDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">{{user.firstname}} {{user.lastname}}</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-form ref="form" v-model="valid">
            <v-row>
              <v-col cols="12">
                <v-text-field label="Password*" type="password" v-model="form.password" :rules="rules.password" required></v-text-field>
              </v-col>
            </v-row>
          </v-form>
        </v-container>
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog()">
          Close
        </v-btn>
        <v-btn color="blue darken-1" :loading="loading" :disabled="loading || !valid" text @click="authenticate()">
          Logon
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" :color="snackbar.color" top>
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="yellow" text v-bind="attrs" @click="snackbar.show = false" >
          Close
        </v-btn>
      </template>
    </v-snackbar>

  </v-dialog>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'
import localStorageService from '@/services/localStorageService'

export default {
  name: 'UserPasswordDialog',
  props: {
    showLogonDialog: Boolean,    
    user: null
  },
  data(){
    return {
      form: {
        password: ''
      },
      rules: {
        password: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 4) || 'Password must be at least 4 characters',        
        ],
      },
      snackbar: {
        show: false,
        text: "",
        timeout: 3000,
        color: ""
      },      
      valid: false,
      loading: false
    }
  },
  methods: {
    closeDialog: function(){
      this.$refs.form.reset();
      this.$emit('close-logon');

    },
    authenticate () {

      // Instead of this timeout, here you can call your API
      if(false){
        this.loading = true;
        window.setTimeout(() => {
          this.loading = false;
          this.closeDialog();
        }, 1500)
        return;
      }

      this.loading = true
      let creds = {
        userId:this.user.userId, 
        email:this.user.email, 
        password:this.form.password
      };

      statTrackerService.authenticate(creds)
          .then((result) => {
            if(result.status === 200){
              
              localStorageService.setCredentialsModel(result.data);

              this.$router.push(`/UserStats`);
              //     this.sbMessage = "Set Token, Redirect";
              //this.$router.push(`/UserStats/${this.user.userId}`);
              //     //console.log(res.data.payload);

            }
          })
          .catch((error) => {
              this.$refs.form.reset();
              this.snackbar.text = error.response.data.detail;
              this.snackbar.color = "red"
              this.snackbar.show = true;
          })
          .finally(() => {
              this.loading = false;
              // this.displaySnackBar = Boolean(this.sbMessage);
          });
    }
  }
}    
</script>