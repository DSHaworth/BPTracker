<template>
  <v-dialog v-model="showCreateDialog" persistent max-width="600px">
    <v-card>
      <v-card-title>
        <span class="headline">Add Weight Stat</span>
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
        <small>*indicates required field</small>
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="closeDialog()">
          Close
        </v-btn>
        <v-btn color="blue darken-1" :loading="loading" :disabled="loading || !valid" text @click="createWeightStat()">
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
  name: 'WeightCreateDialog',
  props: {
    showCreateDialog: Boolean,
    userId: Number
  },
  data(){
    return {
      form: {
        showCreateDialog: false,
        recordDate: '',
        recordTime: '',
        weight: '',
        notes: ''
      },
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
    showCreateDialog(visible) {
      if (visible) {
        // Here you would put something to happen when dialog opens up
        var d = new Date();
        this.form.recordTime = `${d.getHours()}:${d.getMinutes()}`;
        this.form.recordDate = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
      } else {
        //console.log("Dialog was closed!")
      }
    }
  },
  computed: {
  },  
  methods: {
    closeDialog: function(){
      this.$refs.form.reset();
      this.$emit('close-create')
    },
    createWeightStat () {
      let dto = {
        userId:  this.userId,
        recordDateTime: new Date( `${this.form.recordDate} ${this.form.recordTime}`),
        weight: parseFloat(this.form.weight),
        notes: this.form.notes,
      }

      // Instead of this timeout, here you can call your API
      if(false){
        this.loading = true;
        window.setTimeout(() => {
          this.$store.dispatch("addWeightStat", dto);
          this.loading = false;
        }, 1500)
        return;
      }
      
      this.loading = true

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
  }
}    
</script>