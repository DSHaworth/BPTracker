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
        Blood Pressure goes here
      </v-tab-item>

    </v-tabs>

  </v-sheet>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'
import WeightComponent from '@/components/WeightComponent.vue'
import PulseComponent from '@/components/PulseComponent.vue'

export default {
  name: 'UserStats',
  data() { 
    return {
      loading: false,
      weightStats: []
    }
  },  
  methods: {
    getUserWeightStats: function(){
      this.loading = true;
      statTrackerService.getWeightStatsByUser(1)      
        .then((result) => {
          if(result === 200){
            this.weightStats = result.data;
          }
        })
        .catch((error) => {
            console.log(error)
            //console.log(error.response.data.detail);
        })
        .finally(() => {
          this.loading = false;
        });
    }
  },
  components: {
    WeightComponent,
    PulseComponent
  },  
  created() {
    //this.getUserWeightStats();
  }  
}    
</script>

<style scoped lang="scss">
  .card-content{
      text-align: center;
      padding: 25px 0;
  }
</style>