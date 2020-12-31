<template>
  <v-dialog v-if="currentUser" v-model="showLogonDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">{{currentUser.firstname}} {{currentUser.lastname}}</span>
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
import { mapState  } from 'vuex'

export default {
  name: 'UserPasswordDialog',
  props: {
    showLogonDialog: Boolean,
    successAction: null
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
  computed: {
    ...mapState({currentUser: "user"})
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
      
      let creds = {
        userId:this.currentUser.userId, 
        email:this.currentUser.email, 
        password:this.form.password
      };
      
      this.loading = true
      this.$store.dispatch('login', creds)
        .then((result) => {

          switch(true){
            case typeof(this.successAction) === "string":
              this.closeDialog();
              this.$router.push(this.successAction);
              break;

            case typeof(this.successAction) === "function":
              this.closeDialog();
              this.successAction();
              break;

            default:
              this.$refs.form.reset();
              this.snackbar.text = `Unknown action type: ${typeof(this.successAction)}`;
              this.snackbar.color = "red"
              this.snackbar.show = true;    
              break;
          }

        })
        .catch(err => {
          this.$refs.form.reset();
          this.snackbar.text = err.response.data.detail;
          this.snackbar.color = "red"
          this.snackbar.show = true;          
        })
        .then(() => {
          this.loading = false;
        })
    }
  }
}    
</script>