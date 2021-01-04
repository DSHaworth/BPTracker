<template>
    <GChart type="LineChart" :data="getBpChartValues" :options="chartOptions" :resizeDebounce="50"  />
</template>

<script>
import { mapGetters  } from 'vuex'
import { GChart } from "vue-google-charts";
import commonService from '@/services/commonService'

export default {
  name: 'BloodPressureChart',
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
    ...mapGetters(['userBpStats']),
    getBpChartValuesSorted: function(){
        let sortByDate = this.userBpStats
                            .slice() // Make copy of original array (avoids changing original array when sorting)
                            .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime));
        return sortByDate.reverse();
    },           
    getBpChartValues: function(){
        let values = this.getBpChartValuesSorted.map( a => [commonService.formatDateTime(a.recordDateTime), a.sys, a.dia]);
        values.unshift(["DateTime", "Sys", "Dia"]);
        return values;
    }    
  },
  components: {
    GChart
  },  
}
</script>

<style lang="scss" scoped>

</style>