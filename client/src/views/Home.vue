<template>
  <div class="home">
    
    
    <template v-if="users.length">
      <div v-for="user in users" :key="user.userId">
        {{user.firstname}} {{user.lastname}}
      </div>
    </template>    
    <template v-else>
      <span class="md-display-3">Currently no users</span>
    </template>

    <div><md-button class="md-raised md-primary">Create Account</md-button></div>

  </div>
</template>

<script>
import statTrackerService from '@/services/statTrackerService'

export default {
  name: 'Home',
  data() { 
    return {
      users: []
    }
  },
  components: {
    //HelloWorld
  },
  created() {
    console.log('Component has been created!');
    statTrackerService.getUsers()
      .then((res) => {
        if(res.data.isValid){
          console.log(res.data)
          this.users = res.data.payload;
        } else {
          console.log("Error")
          console.log(res);
          console.log(res.data.errorMessage);
        }
        })
        .catch((error) => {
            console.error(error);
        })
        .finally(() => {
          console.log("Finally")
        });
      }
}
</script>

<style lang="scss" scoped>

</style>