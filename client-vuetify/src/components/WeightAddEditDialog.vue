<template>
  <v-dialog v-model="showDialog" max-width="500px" persistent>
    <v-card>
      <v-card-title>
        <span class="headline">{{ formTitle }}</span>
      </v-card-title>

      <v-card-text>
        <v-container>

          <v-form ref="form" v-model="valid">
            <v-row>
              <v-col col="12" md="6">
                <v-menu v-model="menuRecordDate" :close-on-content-click="false" :nudge-right="40" transition="scale-transition" offset-y min-width="290px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field v-model="form.recordDate" label="Record Date" prepend-icon="mdi-calendar" readonly v-bind="attrs" v-on="on"></v-text-field>
                  </template>
                  <v-date-picker v-model="form.recordDate" @input="menuRecordDate = false"></v-date-picker>
                </v-menu>
              </v-col>
              <v-col col="12" md="6">
                <v-menu ref="menu" v-model="menuRecordTime" :close-on-content-click="false" :nudge-right="40" :return-value.sync="form.recordTime" transition="scale-transition" offset-y max-width="290px" min-width="290px">
                  <template v-slot:activator="{ on, attrs }">
                    <v-text-field v-model="form.recordTime" label="Picker in menu" prepend-icon="mdi-clock-time-four-outline" readonly v-bind="attrs" v-on="on"></v-text-field>
                  </template>
                  <v-time-picker v-if="menuRecordTime" v-model="form.recordTime" full-width @click:minute="$refs.menu.save(form.recordTime)" />
                </v-menu>                
              </v-col>              
            </v-row>
            
            <v-row>
              <v-col cols="12" md="6">
                <v-text-field label="Weight*" type="number" v-model="form.weight" :rules="rules.requiredNumber" required></v-text-field>                
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field label="Notes" type="text" v-model="form.notes" ></v-text-field>                
              </v-col>              
            </v-row>
          </v-form>

        </v-container>
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog">
          Close
        </v-btn>
        <v-btn color="blue darken-1" text :loading="loading" :disabled="loading || !valid" @click="addItem">
          Save
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

</template>

<script>
import statTrackerService from '@/services/statTrackerService'
import snackbarService from '@/services/snackbarService'

export default {
  name: 'WeightAddEditDialog',
  props: {
    formTitle: String,
    showDialog: Boolean,
    userId: Number,
    item: Object
  },
  data(){
    return {
      form: {},
      rules: {
        requiredNumber: [
          v => !!v || 'Input is required',
          v => (v && /^[0-9]+([.][0-9]+)?$/g.test(v)) || 'Input must be valid',
        ]
      },
      menuRecordDate: false,
      menuRecordTime: false,
      valid: false,
      loading: false
    }
  },
  watch: {
    showDialog(visible) {
      if (visible) {
        this.form = Object.assign({}, this.item)
      } else {
        //console.log("Dialog was closed!")
      }
    }
  },
  computed: {
  },  
  methods: {
    // Dialog Action Methods
    closeDialog: function(){
      this.$refs.form.reset();
      this.$emit('close-create')
    },
    addItem () {

      let dto = {
        weightId: this.form.weightId,
        userId:  this.form.userId,
        recordDateTime: new Date( `${this.form.recordDate} ${this.form.recordTime}`),
        weight: parseFloat(this.form.weight),
        notes: this.form.notes,
      }

      // https://codepen.io/pen/?editors=1010

      this.loading = true
      if(this.form.weightId){
        
        this.$store.dispatch('updateWeightStat', dto)
          .then(() => {            
            snackbarService.showSuccess({
              text: "Record updated"
            });            
          })
          .catch(err => {
            this.$refs.form.reset();

            console.log(err);

            snackbarService.showError({
              text: err.response.data.detail
            })
          })
          .then(() => {
            this.loading = false;
            this.closeDialog();
          })
      } 
      else {
        
        this.$store.dispatch('addWeightStat', dto)
          .then(() => {
            snackbarService.showSuccess({
              text: "New weight added"
            })
          })
          .catch(err => {
            this.$refs.form.reset();
            snackbarService.showError({
              text: err.response.data.detail
            })
          })
          .then(() => {
            this.loading = false;
          })
      }

      return;

      // Instead of this timeout, here you can call your API
      if(false){
        this.loading = true;
        window.setTimeout(() => {
          this.$store.dispatch("addWeightStat", dto);
          this.loading = false;
        }, 1500)
        return;
      }
    }
  }
}    
</script>