<template>
    <div>
        <template v-if="!loading">
            <form novalidate class="md-layout md-gutter md-alignment-top-center" @submit.prevent="validateUser">
                <md-card class="md-layout-item md-size-50 md-small-size-100">
                    <md-card-header>
                        <div class="md-title">Password</div>
                    </md-card-header>

                    <md-card-content>
                        <div>{{user.firstname}} {{user.lastname}}</div>

                        <md-field :class="getValidationClass('password')">
                            <label for="password">Password</label>
                            <md-input type="password" name="password" id="password" v-model="form.password" :disabled="sending" />
                            <span class="md-error" v-if="!$v.form.password.required">The password is required</span>
                        </md-field>
                    </md-card-content>

                    <md-progress-bar md-mode="indeterminate" v-if="sending" />

                    <md-card-actions>
                        <md-button type="submit" class="md-primary" :disabled="sending">Create user</md-button>
                    </md-card-actions>
                </md-card>

                <md-snackbar :md-active.sync="userSaved">The user {{ user.firstname }} was saved with success!</md-snackbar>

            </form>

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
            user: {},
            loading: false,
            userSaved: false,
            sending: false
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
                    console.log("Error")
                    console.log(res);
                    console.log(res.data.errorMessage);
                }
                })
                .catch((error) => {
                    console.error(error);
                })
                .finally(() => {
                    this.loading = false;
                });
        },
        clearForm () {
            this.$v.$reset()
            this.form.password = null
        },
        saveUser () {
            this.sending = true

            // Instead of this timeout, here you can call your API
            window.setTimeout(() => {
                this.userSaved = true
                this.sending = false
                this.clearForm()
            }, 1500)
        },
        validateUser () {
            this.$v.$touch()

            if (!this.$v.$invalid) {
            this.saveUser()
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