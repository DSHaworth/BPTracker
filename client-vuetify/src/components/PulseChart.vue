<template>
  <GChartCustom
    type="CandlestickChart"
    :data="chartData"
    :options="chartOptions"
    :resizeDebounce="50"
    :firstRowAsData="true"
    @ready="onChartReady"
  />
</template>

<script>
import { mapGetters } from "vuex";
import GChartCustom from "@/components/GChart/GChartCustom.vue";

import commonService from "@/services/commonService";

export default {
  name: "PulseChart",
  data() {
    return {
      chartData: [],
      api: null,
      chartOptions: {
        legend: "none",
        tooltip: { isHtml: true },
        bar: { groupWidth: "5%" }, // Remove space between bars.
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
          width: "100%",
        },
        // width: '100%',
        // //height: '150'
        // //title: "Pulse",
        // //subtitle: "Sales, Expenses, and Profit: 2014-2017"
      },
    };
  },
  watch: {
    api() {
      this.setChartValues();
    },
    getPulseChartValuesSorted() {
      this.setChartValues();
    },
  },
  computed: {
    ...mapGetters(["userPulseStats", 'getPulseChartValuesSorted']),
    formTitle() {
      return this.editedItem.pulseId === 0 ? "Add Item" : "Edit Item";
    },
  },
  methods: {
    setChartValues() {
      if (!this.api) {
        return;
      }

      let sortedDates = this.getPulseChartValuesSorted;
      //let reformatedDates = values.map( a => ({...a, recordDateTime: commonService.formatDate(a.recordDateTime)}) )
      let reformatedDates = sortedDates.map((a) => ({
        recordDateTime: commonService.formatDate(a.recordDateTime),
        pulse: a.pulse,
      }));
      let grouped = commonService.groupBy(
        reformatedDates,
        (rdt) => rdt.recordDateTime
      );

      let chartValues = [];
      grouped.forEach((mapValues, mapKey) => {
        let pulseData = mapValues.map((i) => i.pulse).sort();
        let newRow = [];
        let tooltip =
          pulseData[0] === pulseData[pulseData.length - 1]
            ? `<div style="padding: .5rem; width: 8rem;">Single reading${pulseData[0]}</div>`
            : `<div style="padding: .5rem; width: 8rem;">Highest: ${
                pulseData[pulseData.length - 1]
              } <br/> Lowest: ${pulseData[0]}<div>`;

        newRow.push(
          mapKey,
          pulseData[0],
          pulseData[0],
          pulseData[pulseData.length - 1],
          pulseData[pulseData.length - 1],
          tooltip
        );
        chartValues.push(newRow);
      });

      // https://codesandbox.io/s/my172nvy79?module=/src/App.vue&file=/src/App.vue
      // https://github.com/devstark-com/vue-google-charts/issues/37
      const dataTable = new this.api.visualization.DataTable();
      dataTable.addColumn("string", "data");
      dataTable.addColumn("number", "num1");
      dataTable.addColumn("number", "num2");
      dataTable.addColumn("number", "num3");
      dataTable.addColumn("number", "num4");
      dataTable.addColumn({
        type: "string",
        role: "tooltip",
        p: { html: true },
      });

      dataTable.addRows(chartValues);
      this.chartData = dataTable;
    },
    onChartReady(chart, api) {
      this.api = api;
    },
  },
  components: {
    GChartCustom,
  },
};
</script>

<style lang="scss" scoped>
</style>