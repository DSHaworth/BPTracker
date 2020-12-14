<template>
    <div>
        <template v-if="!loading">
            <template v-if="user">
                <form novalidate class="md-layout md-gutter md-alignment-top-center" @submit.prevent="validateUser">
                    <md-card class="md-layout-item md-size-50 md-small-size-100">
                        <md-card-header>
                            <div class="md-title">Password</div>
                        </md-card-header>

                        <md-card-content>
                            <div>{{user.firstname}} {{user.lastname}}</div>

                            <md-field :class="getValidationClass('password')">
                                <label for="password">Password</label>
                                <md-input type="password" ref="password" name="password" id="password" v-model="form.password" :disabled="sending" />
                                <span class="md-error" v-if="!$v.form.password.required">The password is required</span>
                            </md-field>
                        </md-card-content>

                        <md-progress-bar md-mode="indeterminate" v-if="sending" />

                        <md-card-actions>
                            <md-button to="/" class="md-secondary" :disabled="sending">Cancel</md-button>
                            <md-button type="submit" class="md-primary" :disabled="sending">Login</md-button>
                        </md-card-actions>
                    </md-card>

                    <md-snackbar :md-active.sync="displaySnackBar">{{sbMessage}}</md-snackbar>
                    
                </form>

            </template>
            <template v-if="!user">
                <div>No User</div>
            </template>

        </template>
        <loading-dialog msg="Getting Record" v-bind:showDialog="loading" />
    </div>
</template>

<script>
  import { validationMixin } from 'vuelidate'
  import {
    required
  } from 'vuelidate/lib/validators'

import LoadingDialog from '@/components/LoadingDialog.vue'
import statTrackerService from '@/services/statTrackerService'

export default {
    name: "UserView",
    mixins: [validationMixin],
    data(){
        return{
            form: {
                password: null,
            },
            user: null,
            loading: false,
            displaySnackBar: false,
            sending: false,
            sbMessage: ""
        }
    },
    validations: {
      form: {
        password: {
          required
        },
      }
    },
    methods:{
        getValidationClass (fieldName) {
            const field = this.$v.form[fieldName]

            if (field) {
                return {
                    'md-invalid': field.$invalid && field.$dirty
                }
            }
        },
        getUserById: function(userId){
            this.loading = true;
            statTrackerService.getUserById(userId)      
                .then((res) => {
                if(res.data.isValid){
                    this.user = res.data.payload;
                } else {
                    this.sbMessage = res.data.errorMessage;
                }
                })
                .catch((error) => {
                    this.sbMessage = res.data.errorMessage;
                })
                .finally(() => {
                    this.loading = false;
                    this.displaySnackBar = Boolean(this.sbMessage);
                });
        },
        clearForm () {
            this.$v.$reset()
            this.form.password = null
        },
        login () {

            this.sending = true
            statTrackerService.authenticate({userId:this.user.userId, email:this.user.email, password:this.form.password})
                .then((res) => {
                if(res.data.isValid){
                    this.sbMessage = "Set Token, Redirect";
                    this.$router.push(`/UserStats/${this.user.userId}`);
                    //console.log(res.data.payload);
                } else {
                    this.sbMessage = res.data.errorMessage;
                    this.clearForm();
                    // this.$nextTick(() => {
                    //     //document.getElementById('password').focus();
                    //     console.log(this.$refs.password)
                    //     console.log(this.$refs.password.$el.focus());
                    //     //this.$refs.password.focus()
                    // });
                }
                })
                .catch((error) => {
                    this.sbMessage = res.error;
                })
                .finally(() => {
                    this.sending = false;
                    this.displaySnackBar = Boolean(this.sbMessage);
                });

            // Instead of this timeout, here you can call your API
            // window.setTimeout(() => {
            //     this.userSaved = true
            //     this.sending = false
            //     this.clearForm()
            // }, 1500)
        },
        validateUser () {
            this.$v.$touch()

            if (!this.$v.$invalid) {
                this.login();
            }
        }
    },
    components: {
        LoadingDialog
    },
    created(){
        console.log(this.$route);
        if(this.$route.params.userId){
            this.getUserById(this.$route.params.userId)
        }
    }
}
</script>

<style lang="scss" scoped>
form{
    padding: 2rem;
}

.md-progress-bar {
    position: absolute;
    top: 0;
    right: 0;
    left: 0;
}
</style>