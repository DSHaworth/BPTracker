<template>
  <div class="about">
    <v-card class="mx-auto" style="padding: 1rem;">
        <h1>{{currentUser.firstname}} {{currentUser.lastname}}</h1>

            <div style="display: flex; flex-flow: row wrap; justify-content: flex-start; align-content: flex-start;">
                
                <v-card v-if="userWeightStats.length > 1" class="mt-4 mx-auto" width="33%" min-width="150px;">
                    <v-sheet class="v-sheet--offset mx-auto" elevation="5" max-width="calc(100% - 32px)">
                        <WeightChart />
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        User Weight
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        <!-- From {{ formatDate(userWeightStats[0].recordDateTime) }} -->
                        <!-- To {{ formatDate(userWeightStats[getWeightChartValuesSorted.length - 1].recordDateTime) }} -->
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        <!-- {{getLastRecordedDateDays(getWeightChartValuesSorted[getWeightChartValuesSorted.length - 1])}} -->
                    </span>
                    </v-card-text>
                </v-card>

                <v-card v-if="userPulseStats.length > 2" class="mt-4 mx-auto" width="33%">
                    <v-sheet class="v-sheet--offset mx-auto" elevation="5" max-width="calc(100% - 32px)">                        
                        <PulseChart />
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        User Pulse
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        <!-- From {{ formatDate(userPulseStats[0].recordDateTime) }} -->
                        <!-- To {{ formatDate(userPulseStats[getPulseChartValuesSorted.length - 1].recordDateTime) }} -->
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        <!-- {{getLastRecordedDateDays(getPulseChartValuesSorted[getPulseChartValuesSorted.length - 1])}} -->
                    </span>
                    </v-card-text>
                </v-card>

                <v-card v-if="userBpStats.length >= 2" class="mt-4 mx-auto" width="33%">
                    <v-sheet class="v-sheet--offset mx-auto" elevation="5" max-width="calc(100% - 32px)">
                        <template v-if="userBpStats.length >= 2">
                            <BloodPressureChart />
                        </template>
                        <template v-else>
                            <div style="height: 150px; display: flex; justify-content: center; align-items: center">
                                Not enough data
                            </div>
                        </template>
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        Blood Pressure
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        <!-- From {{ formatDate(userBpStats[0].recordDateTime) }} -->
                        <!-- To {{ formatDate(userBpStats[getBpChartValuesSorted.length - 1].recordDateTime) }} -->
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        <template v-if="userBpStats.length >= 2">
                            <!-- {{getLastRecordedDateDays(getBpChartValuesSorted[getBpChartValuesSorted.length - 1])}} -->
                        </template>
                        <template v-else>
                            Not enough data
                        </template>
                    </span>
                    </v-card-text>
                </v-card>

            </div>
    </v-card>
  </div>
</template>

<script>
import { mapState, mapGetters  } from 'vuex'
import WeightChart from "@/components/WeightChart"
import PulseChart from "@/components/PulseChart"
import BloodPressureChart from "@/components/BloodPressureChart"

import commonService from '@/services/commonService'
import snackbarService from '@/services/snackbarService'
import EventBus from '@/eventBus'

export default {
    name: 'ProfileComponent',
    data () {
        return {
            // loading: false,
            // chartOptions: {
            //     curveType: 'function',
            //     legend: {position: 'none'},
            //     hAxis: { 
            //         textPosition: 'none',                  
            //     },
            //     vAxis: { 
            //         textPosition: 'none',
            //         gridlines: {
            //             color: 'transparent'
            //         },
            //         // viewWindow: {
            //         //     min: 20,
            //         //     max: 300
            //         // },
            //         //ticks: [0, 25, 50, 75, 100] // display labels every 25                    
            //     },
            //     chartArea: {
            //         //left: 40,
            //         // leave room for y-axis labels
            //         width: '100%'
            //     },
            //     width: '100%',
            //     height: '150'
            //     //title: "Pulse",
            //     //subtitle: "Sales, Expenses, and Profit: 2014-2017"
            // }
        }
    },
    computed: {
        ...mapState({currentUser: "user"}),
        ...mapGetters(['userWeightStats', 'userPulseStats', 'userBpStats']),
        // getWeightChartValuesSorted: function(){
        //     let sortByDate = this.userWeightStats
        //                         .slice() // Make copy of original array (avoids changing original array when sorting)
        //                         .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))                                
        //     return sortByDate.reverse();
        // },        
        // getWeightChartValues: function(){
        //     let values = this.getWeightChartValuesSorted.map(a => [this.formatDateTime(a.recordDateTime), parseFloat(a.weight)]);
        //     values.unshift(["DateTime", "Weight"]);
        //     return values;
        // },
        // getPulseChartValuesSorted: function(){
        //     let sortByDate = this.userPulseStats
        //                         .slice() // Make copy of original array (avoids changing original array when sorting)
        //                         .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))
        //     return sortByDate.reverse();
        // },        
        // getPulseChartValues: function(){
        //     let values = this.getPulseChartValuesSorted.map(a => [this.formatDateTime(a.recordDateTime), parseInt(a.pulse)]);
        //     values.unshift(["DateTime", "Pulse"]);
        //     return values;
        // },
        // getBpChartValuesSorted: function(){
        //     let sortByDate = this.userBpStats
        //                         .slice() // Make copy of original array (avoids changing original array when sorting)
        //                         .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime));
        //     return sortByDate.reverse();
        // },           
        // getBpChartValues: function(){
        //     let values = this.getBpChartValuesSorted.map( a => [this.formatDateTime(a.recordDateTime), a.sys, a.dia]);
        //     values.unshift(["DateTime", "Sys", "Dia"]);
        //     return values;
        // }        
    },
    methods: {
        getUserData: function(){
            this.loading = true;
            
            Promise.all([
                this.$store.dispatch('getWeightStat', this.currentUser.userId),
                this.$store.dispatch('getPulseStat', this.currentUser.userId),
                this.$store.dispatch('getBpStat', this.currentUser.userId)
            ]).then((values) => {
                
            })
            .catch(error => {
                if(error.response.status === 401){
                    EventBus.$emit('REAUTHENTICATE', this.getUserData)
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
        formatDate(dateToFormat){
            return commonService.formatDate(dateToFormat);
        },
        // formatDateTime(dateToFormat){
        //     let thisDate = new Date(dateToFormat);
        //     return thisDate.toLocaleString();  
        // },        
        // getLastRecordedDateDays(lastRecordedDate){
        //     let lastDate = new Date(lastRecordedDate.recordDateTime); 
        //     let today = new Date(); 
            
        //     // To calculate the time difference of two dates 
        //     var Difference_In_Time = today.getTime() - lastDate.getTime(); 
            
        //     // To calculate the no. of days between two dates 
        //     let diff = Difference_In_Time / (1000 * 3600 * 24);

        //     if(diff < 1){
        //         return "Last recorded less than a day";
        //     } 
        //     else if (diff < 2)
        //     {
        //         return "Last recorded a day ago";
        //     } 
        //     return `${parseInt(diff)} days ago`;
        // }
    },
    components: {
        WeightChart,
        PulseChart,
        BloodPressureChart
    },    
    created() {
        this.getUserData();
    }  
}
</script>

<style scoped lang="scss">

</style>