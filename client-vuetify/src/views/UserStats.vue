<template>
  <v-sheet elevation="5">

    <v-tabs>

      <v-tab href="#weight">
        Weight
      </v-tab>
      <v-tab-item value="weight">
        Weight Component goes here
      </v-tab-item>

      <v-tab href="#bp">
        Blood Pressure
      </v-tab>
      <v-tab-item value="bp">
        Blood Pressure goes here
      </v-tab-item>

      <v-tab href="#pulse">
        Pulse
      </v-tab>
      <v-tab-item value="pulse">
        Pulse data goes here
      </v-tab-item>

    </v-tabs>

  </v-sheet>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'

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
        .then((res) => {

          console.log("Get Weigth Results")
          console.log(res);

          // if(res.data){

          //   //this.users = res.data;
          // } 
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
  created() {
    this.getUserWeightStats();
  }  
}    
</script>

<style scoped lang="scss">
  .card-content{
      text-align: center;
      padding: 25px 0;
  }
</style>