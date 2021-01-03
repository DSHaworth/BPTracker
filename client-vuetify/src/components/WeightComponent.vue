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

        <v-data-table :headers="headers" :items="userWeightStats" :items-per-page="5" :custom-sort="customSort" class="elevation-1" :loading="loading" loading-text="Loading... Please wait">
          <template v-slot:item.weights="{ item }">
            <span>{{ item.weight.toFixed(1) }}</span>
          </template>
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

        <weight-add-edit-dialog :showDialog="showDialog" :formTitle="formTitle" :item="editedItem" v-on:close-create="onCloseCreate"/>

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
      <GChart type="LineChart" :data="getWeightChartValues" :options="chartOptions" :resizeDebounce="50"  />
    </v-tab-item>
  </v-tabs>

</template>

<script>
import { mapState, mapGetters  } from 'vuex'
import { GChart } from "vue-google-charts";

import WeightAddEditDialog from '@/components/WeightAddEditDialog.vue'
import snackbarService from '@/services/snackbarService'
import commonService from '@/services/commonService'
import EventBus from '@/eventBus'

export default {
  name: 'WeightComponent',
  data () {
    return {
      showDialog: false,
      showDeleteDialog: false,
      loading: false,
      editedItem: {
        weightId: 0,
        userId: 0,
        recordDate: '',
        recordTime: '',
        weight: '',
        notes: '',
      },  
      defaultItem: {
        weightId: 0,
        userId: 0,
        recordDate: '',
        recordTime: '',
        weight: null,
        notes: '',
      },           
      headers: [
        { text: 'Date', value: 'recordDateTime', sortable: false, width: "12rem" },
        { text: 'Weight', value: 'weight', sortable: false, width: "5rem" },
        { text: 'Notes', value: 'notes', sortable: false },
        { text: 'Actions', value: 'actions', sortable: false, align: 'end' }
      ],
      chartOptions: {
        curveType: 'function',
        legend: {position: 'none'},
        hAxis: { 
            //textPosition: 'none',                  
        },
        vAxis: { 
            // textPosition: 'none',
            // gridlines: {
            //     color: 'transparent'
            // },
            // viewWindow: {
            //     min: 20,
            //     max: 300
            // },
            //ticks: [0, 25, 50, 75, 100] // display labels every 25                    
        },
        chartArea: {
            left: 40,
            // leave room for y-axis labels
            width: '100%'
        },
        width: '100%',
        //height: '150'
        //title: "Pulse",
        //subtitle: "Sales, Expenses, and Profit: 2014-2017"
      }
    }
  },
  computed: {
    ...mapState({currentUser: "user"}),
    ...mapGetters(['userWeightStats', 'isLoggedIn']),
    formTitle () {
      return (this.editedItem.weightId === 0) ? "Add Item" : "Edit Item";
    },    
    getWeightChartValuesSorted: function(){
        let sortByDate = this.userWeightStats
                            .slice() // Make copy of original array (avoids changing original array when sorting)
                            .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))                                
        return sortByDate.reverse();
    },        
    getWeightChartValues: function(){
        let values = this.getWeightChartValuesSorted.map(a => [commonService.formatDateTime(a.recordDateTime), parseFloat(a.weight)]);
        values.unshift(["DateTime", "Weight"]);
        return values;
    },    
  },
  methods: {
    // Table Actions
    onShowCreate: function(){
      this.editedItem = this.defaultItem;

      var d = new Date();
      this.defaultItem.recordTime = `${d.getHours()}:${d.getMinutes()}`;
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
    onCloseCreate: function(){
      this.showDialog = false;
    },
    getUserWeightStats: function(){

      this.loading = true;
      this.$store.dispatch('getWeightStat', this.currentUser.userId)
        .then(() => {          
        })
        .catch(error => {
          if(error.response.status === 401){
            EventBus.$emit('REAUTHENTICATE', this.getUserWeightStats)
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
      this.$store.dispatch('deleteWeightStat', this.editedItem)
        .then(() => {     
          snackbarService.showSuccess({
            text: "Weight removed"
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

      this.userWeightStats.sort((a, b) => {
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
    GChart,
    WeightAddEditDialog
  },
  created(){
    this.getUserWeightStats();
  }
}
</script>