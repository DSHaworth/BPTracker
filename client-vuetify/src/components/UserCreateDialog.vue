<template>
  <v-dialog v-model="showCreateDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Create new user</span>
      </v-card-title>
      <v-card-text>
        <v-container>
          <v-form ref="form" v-model="valid">

            <v-row>
              <v-col cols="12" >
                <v-text-field label="E-mail*" type="text" v-model="form.email" :rules="rules.email" required></v-text-field>
              </v-col>              
            </v-row>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field label="First name*" type="text" v-model="form.firstname" :rules="rules.requiredAlpha" required></v-text-field>                
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field label="Last name*" type="text" v-model="form.lastname" :rules="rules.requiredAlpha" required></v-text-field>                
              </v-col>              
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="form.gender" :items="['Male', 'Female']" label="Gender*"></v-select>
              </v-col>

              <v-col cols="12" md="6">                
                <v-menu ref="menu" v-model="menu" :close-on-content-click="false" transition="scale-transition" offset-y min-width="290px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field v-model="form.dob" label="Date of Birth*" prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"></v-text-field>
                  </template>
                  <v-date-picker ref="picker" v-model="form.dob" :max="new Date().toISOString().substr(0, 10)" min="1950-01-01" @change="saveDob"></v-date-picker>
                </v-menu> 
              </v-col>
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-text-field label="Password*" type="password" v-model="form.password" :rules="rules.password" required></v-text-field>
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field label="Confirm Password*" type="password" v-model="form.confirmPassword" :rules="[passwordConfirmationRule]" required></v-text-field>
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
        <v-btn color="blue darken-1" :loading="loading" :disabled="loading || !valid" text @click="createUser()">
          Save
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

export default {
  name: 'UserCreateDialog',
  props: {
    showCreateDialog: Boolean,    
  },
  data(){
    return {
      form: {
        email: '',
        firstname: '',
        lastname: '',
        dob: '',
        password: '',
        confirmPassword: ''
      },
      rules: {
        email: [
          v => !!v || 'E-mail is required',
          v => (v && /.+@.+\..+/.test(v)) || 'E-mail must be valid',
        ],      
        password: [
          v => !!v || 'Password is required',
          v => (v && v.length >= 4) || 'Password must be at least 4 characters',
        ],
        requiredAlpha: [
          v => !!v || 'Input is required',
          v => (v && /^[A-Za-z]+$/.test(v)) || 'Input must be valid',
        ]
      },
      snackbar: {
        show: false,
        text: "",
        timeout: 3000,
        color: ""
      },  
      menu: false,
      valid: false,
      loading: false
    }
  },
  watch: {
    menu (val) {
      val && setTimeout(() => (this.$refs.picker.activePicker = 'YEAR'))
    },
  },
  computed: {
      passwordConfirmationRule() {
        return Boolean((this.form.password && this.form.password) === (this.form.confirmPassword && this.form.confirmPassword)) || 'Password must match';
      }
  },  
  methods: {
    closeDialog: function(){
      this.$refs.form.reset();
      this.$emit('close-create')
    },
    saveDob (date) {
      this.$refs.menu.save(date)
    },    
    createUser () {
      let dto = {
        email: this.form.email,
        firstname: this.form.firstname,
        lastname: this.form.lastname,
        gender: this.form.gender, 
        dob: this.form.dob,
        password: this.form.password,
        confirmPassword: this.form.confirmPassword
      }

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

      statTrackerService.createUser(dto)
        .then((result) => {
          if(result){
              this.sbMessage = "Set Token, Redirect";

              this.snackbar.text = "User created";
              this.snackbar.color_scheme = "success"
              this.snackbar.show = true;

              //this.$router.push(`/UserStats/${this.user.userId}`);
              //console.log(res.data.payload);
          }
        })
        .catch((error) => {
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