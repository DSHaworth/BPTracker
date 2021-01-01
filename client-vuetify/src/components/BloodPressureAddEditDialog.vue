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
                <v-text-field label="Sys*" type="number" v-model="form.sys" :rules="rules.requiredNumber" required
                              pattern="[0-9]" onkeypress="return !(event.charCode == 46)" step="1" />                
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field label="Dia*" type="number" v-model="form.dia" :rules="rules.requiredNumber" required
                              pattern="[0-9]" onkeypress="return !(event.charCode == 46)" step="1" />
              </v-col>              
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="form.arm" :items="armItems" label="Arm*" required :rules="rules.requiredSelect"></v-select>
              </v-col>
              <v-col cols="12" md="6">
                <v-select v-model="form.position" :items="positionItems" label="Position*" required :rules="rules.requiredSelect"></v-select>
              </v-col>              
            </v-row>

            <v-row>
              <v-col cols="12" md="6">
                <v-select v-model="form.activity" :items="activityItems" label="Activity*" required :rules="rules.requiredSelect"></v-select>
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
  name: 'BloodPressureAddEditDialog',
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
          v => (v && /^[0-9]+$/g.test(v)) || 'Input must be valid',
        ],
        requiredSelect: [
          v => !!v || 'Select an item'
        ]
      },
      activityItems: ['General', 'Resting', 'After Exercise', 'Before Exercise'],
      positionItems: ['Sitting', 'Standing', 'Lying down'],
      armItems: ['Left', 'Right'],
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
        bpId: this.form.bpId,
        userId:  this.form.userId,
        recordDateTime: new Date( `${this.form.recordDate} ${this.form.recordTime}`),
        sys: parseInt(this.form.sys),
        dia: parseInt(this.form.dia),
        position: this.form.position,
        arm: this.form.arm,
        activity: this.form.activity,
        notes: this.form.notes,
      }

      // https://codepen.io/pen/?editors=1010
      this.loading = true
      if(this.form.bpId){
        
        this.$store.dispatch('updateBpStat', dto)
          .then(() => {            
            snackbarService.showSuccess({
              text: "Record updated",
              timeout: 1000
            });            
          })
          .catch(err => {           
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
        this.$store.dispatch('addBpStat', dto)
          .then(() => {
            snackbarService.showSuccess({
              text: "New BP added",
              timeout: 1500
            });
            this.$refs.form.reset();
          })
          .catch(err => {
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
          this.$store.dispatch("addPulseStat", dto);
          this.loading = false;
        }, 1500)
        return;
      }
    }
  }
}    
</script>