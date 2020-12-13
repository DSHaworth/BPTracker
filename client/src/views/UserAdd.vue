<template>
  <form novalidate class="md-layout md-gutter md-alignment-top-center" @submit.prevent="validateUser">
    <md-card class="md-layout-item md-size-50 md-small-size-100">
      <md-card-header>
        <div class="md-title">Register</div>
      </md-card-header>

      <md-card-content>

        <md-field :class="getValidationClass('email')">
          <label for="email">Email</label>
          <md-input type="email" name="email" id="email" autocomplete="email" v-model="form.email" :disabled="sending" />
          <span class="md-error" v-if="!$v.form.email.required">The email is required</span>
          <span class="md-error" v-else-if="!$v.form.email.email">Invalid email</span>
        </md-field>


        <div class="md-layout md-gutter">
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('firstName')">
              <label for="first-name">First Name</label>
              <md-input name="first-name" id="first-name" autocomplete="given-name" v-model="form.firstName" :disabled="sending" />
              <span class="md-error" v-if="!$v.form.firstName.required">The first name is required</span>
              <span class="md-error" v-else-if="!$v.form.firstName.minlength">Invalid first name</span>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('lastName')">
              <label for="last-name">Last Name</label>
              <md-input name="last-name" id="last-name" autocomplete="family-name" v-model="form.lastName" :disabled="sending" />
              <span class="md-error" v-if="!$v.form.lastName.required">The last name is required</span>
              <span class="md-error" v-else-if="!$v.form.lastName.minlength">Invalid last name</span>
            </md-field>
          </div>
        </div>

        <div class="md-layout md-gutter">
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('gender')">
              <label for="gender">Gender</label>
              <md-select name="gender" id="gender" v-model="form.gender" md-dense :disabled="sending">
                <md-option></md-option>
                <md-option value="M">M</md-option>
                <md-option value="F">F</md-option>
              </md-select>
              <span class="md-error">The gender is required</span>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('dob')">
              <md-datepicker v-model="form.dob">
                <label>Date of birth</label>
              </md-datepicker>
              <span class="md-error" v-if="!$v.form.dob.required">Date of birth is required</span>
            </md-field>
          </div>
        </div>

        <div class="md-layout md-gutter">
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('password')">
              <label for="password">Password</label>
              <md-input type="password" name="password" id="password" v-model="form.password" :disabled="sending" />
              <span class="md-error" v-if="!$v.form.password.required">Password is required</span>
              <span class="md-error" v-else-if="!$v.form.password.minlength">Invalid password</span>
            </md-field>
          </div>
          <div class="md-layout-item md-small-size-100">
            <md-field :class="getValidationClass('confirmPassword')">
              <label for="confirm-password">Confirm Password</label>
              <md-input type="password" name="confirm-password" id="confirm-password" v-model="form.confirmPassword" :disabled="sending" />
              <span class="md-error" v-if="!$v.form.confirmPassword.required">Confirm password is required</span>
              <span class="md-error" v-else-if="!$v.form.confirmPassword.sameAsPassword">Passwords must match</span>
            </md-field>
          </div>
        </div>

      </md-card-content>

      <md-progress-bar md-mode="indeterminate" v-if="sending" />

      <md-card-actions>
        <md-button to="/" class="md-secondary" :disabled="sending">Cancel</md-button>
        <md-button type="submit" class="md-primary" :disabled="sending">Create user</md-button>
      </md-card-actions>
    </md-card>

    <md-snackbar :md-active.sync="userSaved">The user {{ lastUser }} was saved with success!</md-snackbar>
  </form>

</template>

<script>
  import { validationMixin } from 'vuelidate'
  import {
    required,
    email,    
    minLength,
    maxLength,
    sameAs 
  } from 'vuelidate/lib/validators'

  export default {
    name: 'FormValidation',
    mixins: [validationMixin],
    data: () => ({
      form: {
        firstName: null,
        lastName: null,
        gender: null,
        dob: null,
        email: null,
        password: null,
        confirmPassword: null,
      },
      userSaved: false,
      sending: false,
      lastUser: null
    }),
    validations: {
      form: {
        firstName: {
          required,
          minLength: minLength(3)
        },
        lastName: {
          required,
          minLength: minLength(3)
        },
        dob: {
          required
        },
        gender: {
          required
        },
        email: {
          required,
          email
        },
        password: {
          required,
          minLength: minLength(4)
        },
        confirmPassword: {
          required,
          sameAsPassword: sameAs('password')
        }
      }
    },
    methods: {
      getValidationClass (fieldName) {
        const field = this.$v.form[fieldName]

        if (field) {
          return {
            'md-invalid': field.$invalid && field.$dirty
          }
        }
      },
      clearForm () {
        this.$v.$reset()
        this.form.firstName = null;
        this.form.lastName = null;
        this.form.age = null;
        this.form.gender = null;
        this.form.email = null;
        this.form.password = null;
        this.form.confirmPassword = null;
      },
      saveUser () {
        this.sending = true

        // Instead of this timeout, here you can call your API
        window.setTimeout(() => {
          this.lastUser = `${this.form.firstName} ${this.form.lastName}`
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