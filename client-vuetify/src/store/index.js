import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

import statTrackerService from '@/services/statTrackerService'
import localStorageService from '@/services/localStorageService'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorageService.getToken() || '',
    user : {}
  },
  mutations: {
    auth_request(state){
      state.status = 'loading'
    },
    auth_success(state, token, user){
      state.status = 'success'
      state.token = token
      state.user = user
    },
    auth_error(state){
      state.status = 'error'
    },
    logout(state){
      state.status = ''
      state.token = ''
    }    
  },
  actions: {
    login({commit}, creds){
      return new Promise((resolve, reject) => {
          commit('auth_request')
          statTrackerService.authenticate(creds)
            //axios({url: 'http://localhost:3000/login', data: user, method: 'POST' })
            .then(result => {

                console.log("login success");
                console.log(result);

                const token = result.data.token;
                const user = result.data.user;
                localStorageService.setToken(token);
                //localStorage.setItem('token', token);
                // Add the following line:
                axios.defaults.headers.common['Authorization'] = token;
                commit('auth_success', token, user);
                resolve(result);
            })
            .catch(err => {
                commit('auth_error')
                localStorageService.removeToken();
                reject(err);
            })
      })
    },
    logout({commit}){
      return new Promise((resolve, reject) => {
          commit('logout')
          localStorage.removeItem('token')
          delete axios.defaults.headers.common['Authorization']
          resolve()
      })
    }    
  },
  modules: {
  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
  }  
})
