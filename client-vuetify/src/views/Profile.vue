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
                        From {{ formatDate(getWeightChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getWeightChartValuesSorted[getWeightChartValuesSorted.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        {{getLastRecordedDateDays(getWeightChartValuesSorted[getWeightChartValuesSorted.length - 1].recordDateTime)}}
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
                        From {{ formatDate(getPulseChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getPulseChartValuesSorted[getPulseChartValuesSorted.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        {{getLastRecordedDateDays(getPulseChartValuesSorted[getPulseChartValuesSorted.length - 1].recordDateTime)}}
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
                        From {{ formatDate(getBpChartValuesSorted[0].recordDateTime) }}
                        To {{ formatDate(getBpChartValuesSorted[getBpChartValuesSorted.length - 1].recordDateTime) }}
                    </div>
                    <v-divider class="my-2"></v-divider>
                    <v-icon class="mr-2" small>
                        mdi-clock
                    </v-icon>
                    <span class="caption grey--text font-weight-light">
                        <template v-if="userBpStats.length >= 2">
                            {{getLastRecordedDateDays(getBpChartValuesSorted[getBpChartValuesSorted.length - 1].recordDateTime)}}
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
            loading: false,
        }
    },
    computed: {
        ...mapState({currentUser: "user"}),
        ...mapGetters(['userWeightStats', 'getWeightChartValuesSorted', 'userPulseStats', 'getPulseChartValuesSorted', 'userBpStats', 'getBpChartValuesSorted']),
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
        getLastRecordedDateDays(lastRecordedDate){
            return commonService.getLastRecordedDateDays(lastRecordedDate)
        }
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