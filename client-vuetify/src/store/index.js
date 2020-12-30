import Vue from 'vue'
import Vuex from 'vuex'

import statTrackerService from '@/services/statTrackerService'
import localStorageService from '@/services/localStorageService'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    status: '',
    token: localStorageService.getToken() || '',
    user : localStorageService.getUser() || {},
    weightStats: []
  },
  mutations: {
    auth_request(state){
      state.status = 'loading';
    },
    auth_success(state, token, user){
      state.status = 'success';
      state.token = token;
      state.user = user;
    },
    auth_error(state){
      state.status = 'error';
    },
    logout(state){
      state.status = '';
      state.token = '';
      state.user = null;
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
                const token = result.data.token;
                const user = result.data.user;
                //const weightStats = result.data.weightStats;
                localStorageService.setToken(token);
                localStorageService.setUser(user);
                //localStorage.setItem('token', token);
                // Add the following line:
                //axios.defaults.headers.common['Authorization'] = token;
                //axios.defaults.headers.common['Authorization'] = token;
                commit('auth_success', token, user);                
                resolve(result);
            })
            .catch(err => {
                commit('auth_error');
                localStorageService.removeToken();
                localStorageService.removeUser();
                reject(err);
            })
      })
    },
    logout({commit}){
      return new Promise((resolve, reject) => {
          commit('logout');
          localStorageService.removeToken();
          localStorageService.removeUser();
          resolve();
      })
    },
    // Weights
    getWeightStat({commit}, userId){
      return new Promise((resolve, reject) => {
        statTrackerService.getWeightStatsByUser(userId)
          .then(result => {
            const weightStats = result.data;
            commit('set_weight_stats', weightStats);
            resolve(result);
          })
          .catch(err => {
            reject(err);
          })
      })
    },
    addWeightStat({commit}, weightStat){
      return new Promise((resolve, reject) => {
        statTrackerService.addWeightStatForUser(weightStat)
          .then(result => {
              commit('add_weight_stat', weightStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      })
    }
  },
  modules: {
  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userWeightStats: (state) => {
      return state.weightStats ? state.weightStats : []
    }
  }  
})
