import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
// Third Party
import vuetify from './plugins/vuetify';
import Axios from 'axios'
// Custom
import localStorageService from '@/services/localStorageService'
import './styles/custom.scss';

// https://www.digitalocean.com/community/tutorials/handling-authentication-in-vue-using-vuex
// https://github.com/christiannwamba/vue-auth-vuex/blob/master/src/main.js

Vue.prototype.$http = Axios;

const token = localStorageService.getToken();
if (token) {
  Vue.prototype.$http.defaults.headers.common['Authorization'] = token
}

Vue.config.productionTip = false

new Vue({
  router,
  store,
  vuetify,
  render: h => h(App)
}).$mount('#app')
