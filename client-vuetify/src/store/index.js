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
    weightStats: [],
    pulseStats: [],
    bpStats: [],
  },
  mutations: {
    auth_request(state){
      state.status = 'loading';
    },
    auth_success(state, token){
      state.status = 'success';
      state.token = token;      
    },
    auth_error(state){
      state.status = 'error';
    },
    logout(state){
      state.status = '';
      state.token = '';
      state.user = null;
    },
    set_user(state, user){
      state.user = user;
    },
    // Weight Mutations
    set_weight_stats(state, weightStats){
      state.weightStats = weightStats;
    },
    add_weight_stat(state, weightStat){
      state.weightStats.push(weightStat)
    },
    update_weight_stat(state, weightStat){
      const index = state.weightStats.findIndex(item => item.weightId === weightStat.weightId);
      if (index !== -1){
        state.weightStats.splice(index, 1, weightStat);
      } 
    },
    delete_weight_stat(state, weightStat){
      const index = state.weightStats.findIndex(item => item.weightId === weightStat.weightId);
      if (index !== -1){
        state.weightStats.splice(index, 1);
      }       
    },
    // Pulse Mutations
    set_pulse_stats(state, pulseStats){
      state.pulseStats = pulseStats;
    },
    add_pulse_stat(state, pulseStat){
      state.pulseStats.push(pulseStat)
    },
    update_pulse_stat(state, pulseStat){
      const index = state.pulseStats.findIndex(item => item.pulseId === pulseStat.pulseId);
      if (index !== -1){
        state.pulseStats.splice(index, 1, pulseStat);
      } 
    },
    delete_pulse_stat(state, pulseStat){
      const index = state.pulseStats.findIndex(item => item.pulseId === pulseStat.pulseId);
      if (index !== -1){
        state.pulseStats.splice(index, 1);
      }       
    },
    // Bp Mutations
    set_bp_stats(state, bpStats){
      state.bpStats = bpStats;
    },
    add_bp_stat(state, bpStat){
      state.bpStats.push(bpStat)
    },
    update_bp_stat(state, bpStat){
      const index = state.bpStats.findIndex(item => item.bpId === bpStat.bpId);
      if (index !== -1){
        state.bpStats.splice(index, 1, bpStat);
      } 
    },
    delete_bp_stat(state, bpStat){
      const index = state.bpStats.findIndex(item => item.bpId === bpStat.bpId);
      if (index !== -1){
        state.bpStats.splice(index, 1);
      }       
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

                localStorageService.setToken(token);
                localStorageService.setUser(user);

                // Had to separate these two for Login Password dialog to work right.
                commit('set_user', user);
                commit('auth_success', token);

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
    setUser({commit}, user){
      return new Promise((resolve, reject) => {
        commit('set_user', user);
        localStorageService.setUser(user);
        resolve();
      })
    },
    // Weight Actions
    getWeightStat({commit}, userId){
      return new Promise((resolve, reject) => {
        statTrackerService.getWeightStatsByUser(userId)
          .then(result => {
            
            const weightStats = result.data;
            // const weightStats = result.data.map( a => ({ 
            //   ...a,
            //   recordDateTime: new Date(a.recordDateTime)
            // }));
            
            commit('set_weight_stats', weightStats);
            resolve(result);
          })
          .catch(err => {
            if(err.response.status === 401){
              // commit('logout');
              // localStorageService.removeToken();
              // localStorageService.removeUser();                  
            }
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
      });
    },
    updateWeightStat({commit}, weightStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.updateWeightStatForUser(weightStat)
          .then(result => {
              commit('update_weight_stat', weightStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    },
    deleteWeightStat({commit}, weightStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.deleteWeightStatForUser(weightStat)
          .then(result => {
              commit('delete_weight_stat', weightStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    },
    // Pulse Actions
    getPulseStat({commit}, userId){
      return new Promise((resolve, reject) => {
        statTrackerService.getPulseStatsByUser(userId)
          .then(result => {
            const pulseStats = result.data;
            commit('set_pulse_stats', pulseStats);
            resolve(result);
          })
          .catch(err => {
            reject(err);
          })
      })
    },
    addPulseStat({commit}, pulseStat){
      return new Promise((resolve, reject) => {
        statTrackerService.addPulseStatForUser(pulseStat)
          .then(result => {
            const pulseStat = result.data;
            commit('add_pulse_stat', pulseStat);
            resolve(result);
          })
          .catch(err => {
            reject(err);
          })
      });
    },
    updatePulseStat({commit}, pulseStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.updatePulseStatForUser(pulseStat)
          .then(result => {
              commit('update_pulse_stat', pulseStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    },
    deletePulseStat({commit}, pulseStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.deletePulseStatForUser(pulseStat)
          .then(result => {
              commit('delete_pulse_stat', pulseStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    },
    // BP Actions
    getBpStat({commit}, userId){
      return new Promise((resolve, reject) => {
        statTrackerService.getBpStatsByUser(userId)
          .then(result => {
            const bpStats = result.data;
            commit('set_bp_stats', bpStats);
            resolve(result);
          })
          .catch(err => {
            reject(err);
          })
      })
    },
    addBpStat({commit}, bpStat){
      return new Promise((resolve, reject) => {
        statTrackerService.addBpStatForUser(bpStat)
          .then(result => {
            const bpStat = result.data;
            commit('add_bp_stat', bpStat);
            resolve(result);
          })
          .catch(err => {
            reject(err);
          })
      });
    },
    updateBpStat({commit}, bpStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.updateBpStatForUser(bpStat)
          .then(result => {
              commit('update_bp_stat', bpStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    },
    deleteBpStat({commit}, bpStat){
      //Object.assign(this.desserts[this.editedIndex], this.dto)
      return new Promise((resolve, reject) => {
        statTrackerService.deleteBpStatForUser(bpStat)
          .then(result => {
              commit('delete_bp_stat', bpStat);
              resolve(result);
          })
          .catch(err => {
              reject(err);
          })
      });
    }    
  },
  modules: {
  },
  getters : {
    isLoggedIn: state => !!state.token,
    authStatus: state => state.status,
    userWeightStats: (state) => {
      return state.weightStats ? state.weightStats : []
    },

    getWeightChartValuesSorted: (state) => {
      let sortByDate = state.weightStats
                          .slice() // Make copy of original array (avoids changing original array when sorting)
                          .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime))                                
      return sortByDate.reverse();
    },      

    userPulseStats: (state) => {
      return state.pulseStats ? state.pulseStats : []
    },

    getPulseChartValuesSorted: (state) => {
      let sortByDate = state.pulseStats
        .slice() // Make copy of original array (avoids changing original array when sorting)
        .sort(
          (a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime)
        );
      return sortByDate.reverse();
    },    

    userBpStats: (state) => {
      return state.bpStats ? state.bpStats : []
    },
    getBpChartValuesSorted: (state) => {
      let sortByDate = state.bpStats
                          .slice() // Make copy of original array (avoids changing original array when sorting)
                          .sort((a, b) => Date.parse(b.recordDateTime) - Date.parse(a.recordDateTime));
      return sortByDate.reverse();
    },      
  }  
})
