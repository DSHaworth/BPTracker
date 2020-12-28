<template>
  <v-app>
    <v-main>
      <div id="nav">
        <router-link to="/">Home</router-link> |
        <router-link to="/about">About</router-link>
      </div>
      <div class="router-view">
        <router-view/>
      </div>
    </v-main>
  </v-app>
</template>

<script>
import HelloWorld from './components/HelloWorld';

export default {
  name: 'App',

  components: {
    HelloWorld,
  },

  data: () => ({
    //
  }),
};
</script>

<style scoped lang="scss">
  .router-view{
      padding: .5rem;
  }
</style>