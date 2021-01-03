<template>

  <v-tabs background-color="deep-purple accent-4" dark style="padding: 20px;">

    <v-tabs-slider color="yellow"></v-tabs-slider>

    <v-tab href="#table">
      <v-icon left>
        mdi-table
      </v-icon>      
      Table
    </v-tab>
    <v-tab-item value="table">

      <v-sheet color="white" elevation="2" style="padding: 10px; margin: 10px;">

        <v-toolbar flat>
          <v-toolbar-title>{{currentUser.firstname}} {{currentUser.lastname}}</v-toolbar-title> 
          <v-divider class="mx-4" inset vertical></v-divider>
          <v-spacer></v-spacer>
          <v-btn color="primary" elevation="2" fab small @click="onShowCreate()">
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>
        </v-toolbar>

        <v-data-table :headers="headers" :items="userPulseStats" :items-per-page="5" :custom-sort="customSort" class="elevation-1" :loading="loading" loading-text="Loading... Please wait">
          <template v-slot:item.recordDateTime="{ item }">
            <span>{{ new Date(item.recordDateTime).toLocaleString() }}</span>
          </template>
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="editItem(item)" >
              mdi-pencil
            </v-icon>
            <v-icon small @click="deleteItem(item)">
              mdi-delete
            </v-icon>
          </template>               
        </v-data-table>

        <pulse-add-edit-dialog :showDialog="showDialog" :formTitle="formTitle" :item="editedItem" v-on:close-create="onCloseCreate"/>

        <v-dialog v-model="showDeleteDialog" max-width="500px">
          <v-card>
            <v-card-title class="headline">Are you sure you want to delete this item?</v-card-title>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="closeDelete">Cancel</v-btn>
              <v-btn color="blue darken-1" text @click="deleteItemConfirm">OK</v-btn>
              <v-spacer></v-spacer>
            </v-card-actions>
          </v-card>
        </v-dialog>        

      </v-sheet>  
    </v-tab-item>

    <v-tab href="#chart">
      <v-icon left>
        mdi-chart-box-outline
      </v-icon>      
      Chart
    </v-tab>
    <v-tab-item value="chart">

      <GChartCustom type="CandlestickChart" :data="chartData" :options="chartOptions" :resizeDebounce="50" :firstRowAsData="true" @ready="onChartReady" />

    </v-tab-item>
  </v-tabs>

</template>

<script>
import { mapState, mapGetters  } from 'vuex'
import GChartCustom from "@/components/GChart/GChartCustom.vue";

import PulseAddEditDialog from '@/components/PulseAddEditDialog.vue'
import snackbarService from '@/services/snackbarService'
import commonService from '@/services/commonService'
import EventBus from '@/eventBus'

export default {
  name: 'PulseComponent',
  data () {
    return {
      showDialog: false,
      showDeleteDialog: false,
      loading: false,
      editedItem: {
        pulseId: 0,
        userId: 0,
        recordDate: '',
        recordTime: '',
        pulse: '',
        activity: '',
        notes: '',
      },  
      defaultItem: {
        pulseId: 0,
        userId: 0,
        recordDate: '',
        recordTime: '',
        pulse: null,
        activity: '',
        notes: '',
      },           
      headers: [
        { text: 'Date', value: 'recordDateTime', sortable: false, width: "12rem" },
        { text: 'Pulse', value: 'pulse', sortable: false, width: "4rem" },
        { text: 'Activity', value: 'activity', sortable: false, width: "9rem" },
        { text: 'Notes', value: 'notes', sortable: false },
        { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
      ],
      chartData: [],
      api: null,
      chartOptions: {
        legend: 'none',
        tooltip: {isHtml: true},
        bar: { groupWidth: '5%' }, // Remove space between bars.
        // candlestick: {
        //   fallingColor: { strokeWidth: 0, fill: '#a52714' }, // red
        //   risingColor: { strokeWidth: 0, fill: '#0f9d58' }   // green
        // }        
        hAxis: { 
            //textPosition: 'none',                  
        },
        // vAxis: { 
        //     // textPosition: 'none',
        //     // gridlines: {
        //     //     color: 'transparent'
        //     // },
        //     // viewWindow: {
        //     //     min: 20,
        //     //     max: 300
        //     // },
        //     //ticks: [0, 25, 50, 75, 100] // display labels every 25                    
        // },
        chartArea: {
            left: 40,
            // leave room for y-axis labels
            width: '100%'
        },
        // width: '100%',
        // //height: '150'
        // //title: "Pulse",
        // //subtitle: "Sales, Expenses, and Profit: 2014-2017"
      }
    }
  },
  watch: {
    api() {
      this.setChartValues();
    },
    getPulseChartValuesSorted(){
      this.setChartValues();
    }
  },  
  computed: {
    ...mapState({currentUser: "user"}),
    ...mapGetters(['userPulseStats', 'isLoggedIn']),
    formTitle () {
      return (this.editedItem.pulseId === 0) ? "Add Item" : "Edit Item";
    },    
    getPulseChartValuesSorted: function(){
      let sortByDate = this.userPulseStats
                          .slice() // Make copy of original array (avoids changing original array when sorting)
                          .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))
      return sortByDate.reverse();
    },        
  },
  methods: {
    // Table Actions
    onShowCreate: function(){
      this.editedItem = this.defaultItem;

      var d = new Date();
      this.defaultItem.recordTime = `${d.getHours()}:${('0'+d.getMinutes()).slice(-2)}`;
      this.defaultItem.recordDate = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`
      this.editedItem.userId = this.currentUser.userId

      this.showDialog = true;      
    },
    editItem (item) {
      this.editedItem = Object.assign({}, item)

      var d = new Date(item.recordDateTime);
      this.editedItem.recordTime = `${d.getHours()}:${d.getMinutes()}`;
      this.editedItem.recordDate = `${d.getFullYear()}-${d.getMonth() + 1}-${d.getDate()}`;      
      this.editedItem.userId = this.currentUser.userId;

      this.showDialog = true;
    },
    setChartValues(){

      if(!this.api){
        return;
      }

      let sortedDates = this.getPulseChartValuesSorted;
      //let reformatedDates = values.map( a => ({...a, recordDateTime: commonService.formatDate(a.recordDateTime)}) )
      let reformatedDates = sortedDates.map( a => ({recordDateTime: commonService.formatDate(a.recordDateTime), pulse: a.pulse}) )
      let grouped = commonService.groupBy(reformatedDates, rdt => rdt.recordDateTime)

      let chartValues = []
      grouped.forEach( (mapValues, mapKey) => {
        let pulseData = mapValues.map( i => i.pulse).sort();
        let newRow = [];
        let tooltip = pulseData[0] === pulseData[pulseData.length-1] 
                      ? `<div style="padding: .5rem; width: 8rem;">Single reading${pulseData[0]}</div>`
                      : `<div style="padding: .5rem; width: 8rem;">Highest: ${pulseData[pulseData.length-1]} <br/> Lowest: ${pulseData[0]}<div>`

        newRow.push(mapKey, pulseData[0], pulseData[0], pulseData[pulseData.length-1], pulseData[pulseData.length-1], tooltip);
        chartValues.push(newRow);
      })
      
      // https://codesandbox.io/s/my172nvy79?module=/src/App.vue&file=/src/App.vue
      // https://github.com/devstark-com/vue-google-charts/issues/37
      const dataTable = new this.api.visualization.DataTable();
      dataTable.addColumn('string', 'data');
      dataTable.addColumn('number', 'num1');
      dataTable.addColumn('number', 'num2');
      dataTable.addColumn('number', 'num3');
      dataTable.addColumn('number', 'num4');
      dataTable.addColumn({
        type: 'string',
        role: 'tooltip',
        p: { 'html': true }
      });

      dataTable.addRows(chartValues);
      this.chartData = dataTable;
    },
    onChartReady (chart, api) {
      this.api = api;
    },    
    onCloseCreate: function(){
      this.showDialog = false;
    },
    getUserPulseStats: function(){

      this.loading = true;
      this.$store.dispatch('getPulseStat', this.currentUser.userId)
        .then(() => {          
        })
        .catch(error => {
          if(error.response.status === 401){
            EventBus.$emit('REAUTHENTICATE', this.getUserPulseStats)
          }
          else {
            snackbarService.showError({
              text: error.response.data.detail,
            })
          }
        })
        .then(() => {
          this.loading = false;
        })      
    },
    // DELETE START
    deleteItem (item) {
      this.editedItem = Object.assign({}, item)
      this.editedItem.userId = this.currentUser.userId;
      this.showDeleteDialog = true
    },
    closeDelete () {
      this.showDeleteDialog = false
    },
    deleteItemConfirm () {

      this.loading = true;
      this.$store.dispatch('deletePulseStat', this.editedItem)
        .then(() => {     
          snackbarService.showSuccess({
            text: "Pulsee stat removed"
          });              
        })
        .catch(err => {
          snackbarService.showError({
            text: err.response.data.detail
          });          
        })
        .then(() => {
          this.loading = false;
          this.closeDelete();
        })
    },
    //https://codepen.io/mmia/pen/jOPyXad?editors=1010
    customSort: function(items, index, isDesc) {

      this.userPulseStats.sort((a, b) => {
          if (index[0]=='recordDateTime') {
            if (!isDesc[0]) {
                return new Date(b[index]) - new Date(a[index]);
            } else {
                return new Date(a[index]) - new Date(b[index]);
            }
          }
          else {
            if(typeof a[index] !== 'undefined'){
              if (!isDesc[0]) {
                 return a[index].toLowerCase().localeCompare(b[index].toLowerCase());
              }
              else {
                  return b[index].toLowerCase().localeCompare(a[index].toLowerCase());
              }
            }
          }
      });
      return items;
    }
  },
  components: {
    GChartCustom,
    PulseAddEditDialog
  },
  created(){
    this.getUserPulseStats();
  }
}
</script>

<style lang="scss" scoped>

</style>