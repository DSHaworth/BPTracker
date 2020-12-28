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
                <v-text-field label="Password*" type="password" v-model="form.password" :rules="passwordRules" required></v-text-field>
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
  </v-dialog>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'

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
      passwordRules: [
        v => !!v || 'Password is required',
        v => v.length >= 4 || 'Password must be at least 4 characters',        
      ],
      valid: false,
      loading: false
    }
  },
  methods: {
    closeDialog: function(){
      this.$emit('close-logon')
    },
    authenticate () {

      // Instead of this timeout, here you can call your API
      if(false){
        this.loading = true;
        window.setTimeout(() => {
          this.loading = false;
          this.$emit('close-logon')
        //     this.userSaved = true        
        //     this.clearForm()
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

            console.log("Logon result")
            console.log(result);

            // if(result.data.isValid){
            //     this.sbMessage = "Set Token, Redirect";
            //     this.$router.push(`/UserStats/${this.user.userId}`);
            //     //console.log(res.data.payload);
            // }
          })
          .catch((error) => {
              // this.sbMessage = res.error;
              alert(error);
              console.log(error);
          })
          .finally(() => {
              this.loading = false;
              // this.displaySnackBar = Boolean(this.sbMessage);
          });
    }
  }
}    
</script>