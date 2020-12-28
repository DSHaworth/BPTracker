import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// Third Party
import vuetify from './plugins/vuetify';
// Custom
import './styles/custom.scss';

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
