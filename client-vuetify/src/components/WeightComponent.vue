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
        <div class='right-side' style="margin-bottom: .5rem;">  

          <v-btn color="primary" elevation="2" fab small @click="onShowCreate()">
            <v-icon dark>
              mdi-plus
            </v-icon>
          </v-btn>

        </div>
        <v-data-table :headers="headers" :items="userWeightStats" :items-per-page="5" :custom-sort="customSort" class="elevation-1">
          <template v-slot:item.recordDateTime="{ item }">
            <span>{{ new Date(item.recordDateTime).toLocaleString() }}</span>
          </template>          
        </v-data-table>
        <weight-create-dialog :showCreateDialog="showCreateDialog" v-on:close-create="onCloseCreate" :userId="currentUser.userId"/>
      </v-sheet>  

    </v-tab-item>

    <v-tab href="#chart">
      <v-icon left>
        mdi-chart-box-outline
      </v-icon>      
      Chart
    </v-tab>
    <v-tab-item value="chart">

      <v-sparkline
        :value="getChartValues"
        :gradient="sparklineConfig.gradient"
        :smooth="sparklineConfig.radius || false"
        :padding="sparklineConfig.padding"
        :line-width="sparklineConfig.width"
        :stroke-linecap="sparklineConfig.lineCap"
        :gradient-direction="sparklineConfig.gradientDirection"
        :fill="sparklineConfig.fill"
        :type="sparklineConfig.type"
        :auto-line-width="sparklineConfig.autoLineWidth"        
        auto-draw
      ></v-sparkline>

    </v-tab-item>

    <v-snackbar v-model="snackbar.show" :timeout="snackbar.timeout" :color="snackbar.color" top>
      {{ snackbar.text }}
      <template v-slot:action="{ attrs }">
        <v-btn color="yellow" text v-bind="attrs" @click="snackbar.show = false" >
          Close
        </v-btn>
      </template>
    </v-snackbar>

  </v-tabs>

</template>

<script>
import WeightCreateDialog from '@/components/WeightCreateDialog.vue'
import { mapState, mapGetters  } from 'vuex'

export default {
  name: 'WeightComponent',
  data () {
    return {
      showCreateDialog: false,
      snackbar: {
        show: false,
        text: "",
        timeout: 3000,
        color: ""
      },  
      headers: [
        { text: 'Date', value: 'recordDateTime' },
        { text: 'Weight', value: 'weight' },
        { text: 'Notes', value: 'notes', sortable: false }
      ],
      sparklineConfig: {
        width: 2,
        radius: 10,
        padding: 8,
        lineCap: 'round',
        gradient: [
          ['#222'],
          ['#42b3f4'],
          ['red', 'orange', 'yellow'],
          ['purple', 'violet'],
          ['#00c6ff', '#F0F', '#FF0'],
          ['#f72047', '#ffd200', '#1feaea'],
        ],
        value: [0, 2, 5, 9, 5, 10, 3, 5, 0, 0, 1, 8, 2, 9, 0],
        gradientDirection: 'top',
        fill: false,
        type: 'trend',
        autoLineWidth: false,        
      }
    }
  },
  computed: {
    ...mapState({currentUser: "user"}),
    ...mapGetters(['userWeightStats', 'isLoggedIn']),
    getChartValues: function(){
      let sortByDate = this.userWeightStats
                        .slice() // Make copy of original array (avoids changing original array when sorting)
                        .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))
                        .map(a => parseFloat(a.weight));  // Return only weight field
      return sortByDate.reverse();
    }
  },
  methods: {
    onShowCreate: function(){
      
      this.showCreateDialog = true;

      //console.log("IsLoggedOn?: " + this.$store.getters.isLoggedIn);
      console.log("IsLoggedOn?: " + this.isLoggedIn);

      //this.$store.dispatch("addWeightStat", {"weightId": 1, "recordDateTime": new Date(), "weight": 188.3, "notes": ""});

      //this.showCreateDialog = true;
    },
    onCloseCreate: function(){
      this.showCreateDialog = false;
    },
    getUserWeightStats: function(){
      this.$store.dispatch('getWeightStat', this.currentUser.userId)
        .then(() => {
          // this.closeDialog();
          // this.$router.push('/UserStats');
        })
        .catch(err => {
          //this.snackbar.text = err.response.data.detail;
          console.log("err");
          console.log(err);

          this.snackbar.text = err.response.data.detail;
          this.snackbar.color = "red"
          this.snackbar.show = true;          
        })
        .then(() => {
          //this.loading = false;
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
    WeightCreateDialog
  },
  created(){
    this.getUserWeightStats();
  }
}
</script>