<template>
  <v-sheet color="white" elevation="10" style="padding: 10px;">
    <div class='right-side'>  

      <v-btn color="primary" elevation="2" fab small @click="onShowCreate()">
        <v-icon dark>
          mdi-plus
        </v-icon>
      </v-btn>

    </div>
    <v-data-table :headers="headers" :items="this.$store.getters.userWeightStats" :items-per-page="5" class="elevation-1" />
    <weight-create-dialog :showCreateDialog="showCreateDialog" v-on:close-create="onCloseCreate"/>
  </v-sheet>  
</template>

<script>
import WeightCreateDialog from '@/components/WeightCreateDialog.vue'

export default {
  name: 'WeightComponent',
  data () {
    return {
      showCreateDialog: false,
      headers: [
        { text: 'Date', value: 'recordDateTime' },
        { text: 'Weight', value: 'weight' },
        { text: 'Notes', value: 'notes' }
      ],
    }
  },
  methods: {
    onShowCreate: function(){
      
      this.showCreateDialog = true;

      console.log("IsLoggedOn?: " + this.$store.getters.isLoggedIn);

      //this.$store.dispatch("addWeightStat", {"weightId": 1, "recordDateTime": new Date(), "weight": 188.3, "notes": ""});

      //this.showCreateDialog = true;
    },
    onCloseCreate: function(){
      this.showCreateDialog = false;
    }      
  },
  components: {
    WeightCreateDialog
  }
}
</script>