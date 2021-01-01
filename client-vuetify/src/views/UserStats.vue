<template>
  <v-sheet elevation="5">

    <v-tabs>

      <v-tab href="#weight">
        Weight
      </v-tab>
      <v-tab-item value="weight">
        <WeightComponent />
      </v-tab-item>

      <v-tab href="#pulse">
        Pulse
      </v-tab>
      <v-tab-item value="pulse">
        <PulseComponent />
      </v-tab-item>

      <v-tab href="#bp">
        Blood Pressure
      </v-tab>
      <v-tab-item value="bp">
        <BloodPressureComponent />
      </v-tab-item>

    </v-tabs>

  </v-sheet>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'
import WeightComponent from '@/components/WeightComponent.vue'
import PulseComponent from '@/components/PulseComponent.vue'
import BloodPressureComponent from '@/components/BloodPressureComponent.vue'

export default {
  name: 'UserStats',
  data() { 
    return {
    }
  },  
  methods: {
  },
  components: {
    WeightComponent,
    PulseComponent,
    BloodPressureComponent
  },  
  created() {
  }  
}    
</script>

<style scoped lang="scss">

</style>