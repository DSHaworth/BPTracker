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
    user : {},
    weightStats: []
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
    },
    /////
    set_weight_stats(state, weightStats){
      state.weightStats = weightStats
    },
    add_weight_stat(state, weightStat){
      state.weightStats.push(weightStat)
    }
  },
  actions: {
    login({commit}, creds){
      return new Promise((resolve, reject) => {
          commit('auth_request')
          statTrackerService.authenticate(creds)
            .then(result => {

                console.log("login success");
                console.log(result);

                const token = result.data.token;
                const user = result.data.user;
                const weightStats = result.data.weightStats;
                localStorageService.setToken(token);
                //localStorage.setItem('token', token);
                // Add the following line:
                axios.defaults.headers.common['Authorization'] = token;
                commit('auth_success', token, user);
                commit('set_weight_stats', weightStats)
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
    },
    addWeightStat({commit}, weightStat){
      commit('add_weight_stat', weightStat);
    }
  },
  modules: {
  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userWeightStats: (state) => {
      console.log("weight stats");
      console.log(state.weightStats);

      if(state.weightStats){
        return state.weightStats;
      }
      return [];
    }
  }  
})
