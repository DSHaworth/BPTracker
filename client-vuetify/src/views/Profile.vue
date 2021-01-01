<template>
  <div class="about">
    <v-card :loading="loading" class="mx-auto" style="padding: 1rem;">
        <h1>{{currentUser.firstname}} {{currentUser.lastname}}</h1>

            <div style="display: flex; flex-flow: row wrap; justify-content: flex-start; align-content: flex-start;">
                <v-card v-if="getWeightChartValues.length > 1" class="mt-4 mx-auto" max-width="400">
                    <v-sheet class="v-sheet--offset mx-auto" color="cyan" elevation="12" max-width="calc(100% - 32px)">
                        <v-sparkline
                            v-if="getWeightChartValues.length > 1"
                            :value="getWeightChartValues"
                            :gradient="sparklineConfig.gradient"
                            :smooth="sparklineConfig.radius || false"
                            :padding="sparklineConfig.padding"
                            :line-width="sparklineConfig.width"
                            :stroke-linecap="sparklineConfig.lineCap"
                            :gradient-direction="sparklineConfig.gradientDirection"
                            :fill="sparklineConfig.fill"
                            :type="sparklineConfig.type"
                            :auto-line-width="sparklineConfig.autoLineWidth"        
                            auto-draw />
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        User Weight
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        From {{ formatDate(getWeightChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getWeightChartValuesSorted[getWeightChartValues.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        {{getLastRecordedDateDays(getWeightChartValuesSorted[getWeightChartValuesSorted.length - 1])}}
                    </span>
                    </v-card-text>
                </v-card>

                <v-card v-if="getPulseChartValues.length > 2" class="mt-4 mx-auto" max-width="400">
                    <v-sheet class="v-sheet--offset mx-auto" color="cyan" elevation="12" max-width="calc(100% - 32px)">
                        <v-sparkline                            
                            :value="getPulseChartValues"
                            :gradient="sparklineConfig.gradient"
                            :smooth="sparklineConfig.radius || false"
                            :padding="sparklineConfig.padding"
                            :line-width="sparklineConfig.width"
                            :stroke-linecap="sparklineConfig.lineCap"
                            :gradient-direction="sparklineConfig.gradientDirection"
                            :fill="sparklineConfig.fill"
                            :type="sparklineConfig.type"
                            :auto-line-width="sparklineConfig.autoLineWidth"        
                            auto-draw />
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        User Pulse
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        From {{ formatDate(getPulseChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getPulseChartValuesSorted[getWeightChartValues.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        {{getLastRecordedDateDays(getPulseChartValuesSorted[getPulseChartValuesSorted.length - 1])}}
                    </span>
                    </v-card-text>
                </v-card>

                <v-card v-if="getBpChartValues.length > 2" class="mt-4 mx-auto" max-width="400">
                    <v-sheet class="v-sheet--offset mx-auto" color="cyan" elevation="12" max-width="calc(100% - 32px)">
                        <v-sparkline                            
                            :value="getBpChartValues"
                            :gradient="sparklineConfig.gradient"
                            :smooth="sparklineConfig.radius || false"
                            :padding="sparklineConfig.padding"
                            :line-width="sparklineConfig.width"
                            :stroke-linecap="sparklineConfig.lineCap"
                            :gradient-direction="sparklineConfig.gradientDirection"
                            :fill="sparklineConfig.fill"
                            :type="sparklineConfig.type"
                            :auto-line-width="sparklineConfig.autoLineWidth"        
                            auto-draw />
                    </v-sheet>
                    <v-card-text class="pt-0">
                    <div class="title font-weight-light mb-2">
                        User Pulse
                    </div>
                    <div class="subheading font-weight-light grey--text">
                        From {{ formatDate(getBpChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getBpChartValuesSorted[getWeightChartValues.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        {{getLastRecordedDateDays(getBpChartValuesSorted[getBpChartValuesSorted.length - 1])}}
                    </span>
                    </v-card-text>
                </v-card>

            </div>
    </v-card>
  </div>
</template>

<script>
import { mapState, mapGetters  } from 'vuex'
import snackbarService from '@/services/snackbarService'
import EventBus from '@/eventBus'

export default {
    name: 'ProfileComponent',
    data () {
        return {
            loading: false,
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
        ...mapGetters(['userWeightStats', 'userPulseStats', 'userBpStats', 'isLoggedIn']),
        getWeightChartValuesSorted: function(){
            let sortByDate = this.userWeightStats
                                .slice() // Make copy of original array (avoids changing original array when sorting)
                                .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))                                
            return sortByDate.reverse();
        },        
        getWeightChartValues: function(){
            return this.getWeightChartValuesSorted.map(a => parseFloat(a.weight));  // Return only pulse field
        },
        getPulseChartValuesSorted: function(){
            let sortByDate = this.userPulseStats
                                .slice() // Make copy of original array (avoids changing original array when sorting)
                                .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))
            return sortByDate.reverse();
        },        
        getPulseChartValues: function(){
            return this.getPulseChartValuesSorted.map(a => parseInt(a.pulse));  // Return only pulse field
        },
        getBpChartValuesSorted: function(){
            let sortByDate = this.userBpStats
                                .slice() // Make copy of original array (avoids changing original array when sorting)
                                .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime));
            return sortByDate.reverse();
        },           
        getBpChartValues: function(){
            return this.getBpChartValuesSorted.map(a => parseInt(a.sys));  // Return only pulse field
        }        
    },
    methods: {
        getUserData: function(){
            this.loading = true;
            
            Promise.all([
                this.$store.dispatch('getWeightStat', this.currentUser.userId),
                this.$store.dispatch('getPulseStat', this.currentUser.userId),
                this.$store.dispatch('getBpStat', this.currentUser.userId)
            ]).then((values) => {
                console.log(values[0]);
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
            //return new Date(dateToFormat).toDateString(); 
            return new Date(dateToFormat).toLocaleDateString(); 
        },
        getLastRecordedDateDays(lastRecordedDate){
            let lastDate = new Date(lastRecordedDate.recordDateTime); 
            let today = new Date(); 
            
            console.log("lastDate: " + lastDate);
            console.log("today: " + today)

            // To calculate the time difference of two dates 
            var Difference_In_Time = today.getTime() - lastDate.getTime(); 
            
            // To calculate the no. of days between two dates 
            let diff = Difference_In_Time / (1000 * 3600 * 24);

            if(diff < 1){
                return "Last recorded less than a day";
            } 
            else if (diff < 2)
            {
                return "Last recorded a day ago";
            } 
            return `${parseInt(diff)} days ago`;
        }
    },
    created() {
        this.getUserData();
    }  
}
</script>

<style scoped lang="scss">

</style>