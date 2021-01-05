<template>
    <GChart type="LineChart" :data="getWeightChartValues" :options="chartOptions" :resizeDebounce="50"  />
</template>

<script>
import { mapGetters  } from 'vuex'
import { GChart } from "vue-google-charts";

import commonService from '@/services/commonService'

export default {
  name: 'WeightChart',
  data () {
    return {
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
    ...mapGetters(['userWeightStats', 'getWeightChartValuesSorted']),
    getWeightChartValues: function(){
        let values = this.getWeightChartValuesSorted.map(a => [commonService.formatDateTime(a.recordDateTime), parseFloat(a.weight)]);
        values.unshift(["DateTime", "Weight"]);
        return values;
    },    
  },  
  components: {
    GChart
  },  
}
</script>

<style lang="scss" scoped>

</style>