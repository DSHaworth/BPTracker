<template>
  <div class="home">
    
  <pre><code>{{users}}</code></pre>

  </div>
</template>

<script>
// @ is an alias to /src
import statTrackerService from '@/services/statTrackerService'

export default {
  name: 'Home',
  data() { 
    return {
      loading: false,
      users: []
    }
  },
  methods: {
    getUsers: function(){
      this.loading = true;
      statTrackerService.getUsers()      
        .then((res) => {
          if(res.data){
            console.log(res.data)
            this.users = res.data;
          } 
          })
          .catch((error) => {
              console.error(error);
              alert(error);
          })
          .finally(() => {
            this.loading = false;
          });
        }
  },    
  components: {
    
  },
  created() {
    this.getUsers();
    // this.loading = true;
    // setTimeout(this.getUsers, 10000);
  }  
}
</script>
